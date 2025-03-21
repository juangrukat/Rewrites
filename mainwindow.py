# This Python file uses the following encoding: utf-8
import sys
import os
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QPushButton, QLabel, QLineEdit, QTextBrowser
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow
from database import Database
from openai_api import OpenAIAPI

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.db = Database()
        
        # Get model from database if available
        model = self.db.get_model()
        self.openai_api = OpenAIAPI(model=model)
        
        # Set up API key from database if available
        api_key = self.db.get_api_key()
        if api_key:
            self.openai_api.set_api_key(api_key)
            self.ui.apifield.setEchoMode(QLineEdit.Password)  # Set to password mode
            self.ui.apifield.setText(api_key)
        
        # Replace QTextEdit with QTextBrowser for markdown rendering
        self.setup_markdown_viewer()
        
        # Connect UI signals to slots
        self.ui.sendopenai.clicked.connect(self.send_to_openai)
        self.ui.pushButton_random.clicked.connect(self.load_random_excerpt)
        self.ui.apisave.clicked.connect(self.save_api_key)
        
        # Add navigation buttons for excerpts
        self.setup_navigation_buttons()
        
        # Set up prompt combo box
        self.setup_prompt_combo_box()
        
        # Current excerpt ID
        self.current_excerpt_id = None
        
        # Add import CSV button and other UI elements to settings tab
        self.setup_settings_ui()
        
        # Apply font settings if available
        self.apply_font_settings()


    def setup_prompt_combo_box(self):
        """Set up the prompt combo box with default templates"""
        # Get default prompt templates
        default_templates = self.openai_api.get_default_prompt_templates()
        
        # Add default templates to combo box
        for name in default_templates.keys():
            self.ui.comboBox_prompt.addItem(name)
        
        # Get saved prompts from database
        saved_prompts = self.db.get_all_prompts()
        for prompt in saved_prompts:
            self.ui.comboBox_prompt.addItem(prompt[1])  # prompt[1] is the name
    
    def setup_settings_ui(self):
        """Set up all UI elements in the settings tab"""
        # API key label
        self.api_label = QLabel("API Key:", self.ui.Settings)
        self.api_label.setGeometry(30, 30, 100, 16)
        self.api_label.show()
        
        # Import CSV button
        self.import_button = QPushButton("Import CSV", self.ui.Settings)
        self.import_button.setGeometry(200, 100, 100, 32)
        self.import_button.clicked.connect(self.import_csv)
        self.import_button.show()
        
        # Export section label
        self.export_label = QLabel("Export Options:", self.ui.Settings)
        self.export_label.setGeometry(350, 80, 150, 16)
        self.export_label.show()
        
        # Export to CSV button
        self.export_csv_button = QPushButton("Export to CSV", self.ui.Settings)
        self.export_csv_button.setGeometry(350, 100, 120, 32)
        self.export_csv_button.clicked.connect(self.export_to_csv)
        self.export_csv_button.show()
        
        # Export to JSON button
        self.export_json_button = QPushButton("Export to JSON", self.ui.Settings)
        self.export_json_button.setGeometry(480, 100, 120, 32)
        self.export_json_button.clicked.connect(self.export_to_json)
        self.export_json_button.show()
        
        # Add refresh models button
        self.refresh_models_button = QPushButton("Refresh Models", self.ui.Settings)
        self.refresh_models_button.setGeometry(300, 150, 120, 32)
        self.refresh_models_button.clicked.connect(self.fetch_and_update_models)
        self.refresh_models_button.show()
        
        # Clear Database button
        self.clear_db_button = QPushButton("Clear Database", self.ui.Settings)
        self.clear_db_button.setGeometry(430, 150, 120, 32)  # Changed X position from 350 to 430
        self.clear_db_button.clicked.connect(self.clear_database)
        self.clear_db_button.show()
        
        # Model selection
        self.model_label = QLabel("Select Model:", self.ui.Settings)
        self.model_label.setGeometry(30, 150, 100, 16)
        self.model_label.show()
        
        from PySide6.QtWidgets import QComboBox
        self.model_combo = QComboBox(self.ui.Settings)
        self.model_combo.setGeometry(140, 150, 150, 32)
        
        # Load models from database
        saved_models = self.db.get_models()
        self.model_combo.addItems(saved_models)
        
        # Set current model from database
        current_model = self.db.get_model()
        index = self.model_combo.findText(current_model)
        if index >= 0:
            self.model_combo.setCurrentIndex(index)
        
        self.model_combo.currentTextChanged.connect(self.save_model)
        self.model_combo.show()
        
        # Prompt template selection
        self.prompt_label = QLabel("Select Prompt Template:", self.ui.Settings)
        self.prompt_label.setGeometry(30, 200, 150, 16)
        self.prompt_label.show()
        
        # Load prompt from file button
        self.load_prompt_button = QPushButton("Load Prompt File", self.ui.Settings)
        self.load_prompt_button.setGeometry(200, 220, 120, 32)
        self.load_prompt_button.clicked.connect(self.load_prompt_file)
        self.load_prompt_button.show()
        
        # Clear prompts button
        self.clear_prompts_button = QPushButton("Clear Prompts", self.ui.Settings)
        self.clear_prompts_button.setGeometry(330, 220, 120, 32)
        self.clear_prompts_button.clicked.connect(self.clear_prompts)
        self.clear_prompts_button.show()
        
        # Font settings
        self.font_label = QLabel("Font Settings:", self.ui.Settings)
        self.font_label.setGeometry(30, 270, 100, 16)
        self.font_label.show()
        
        # Font family selection
        self.font_family_label = QLabel("Font Family:", self.ui.Settings)
        self.font_family_label.setGeometry(40, 300, 100, 16)
        self.font_family_label.show()
        
        from PySide6.QtGui import QFontDatabase
        self.font_family_combo = QComboBox(self.ui.Settings)
        self.font_family_combo.setGeometry(140, 300, 150, 32)
        font_families = QFontDatabase().families()
        self.font_family_combo.addItems(font_families)
        
        # Font size selection
        self.font_size_label = QLabel("Font Size:", self.ui.Settings)
        self.font_size_label.setGeometry(40, 340, 100, 16)
        self.font_size_label.show()
        
        from PySide6.QtWidgets import QSpinBox
        self.font_size_spin = QSpinBox(self.ui.Settings)
        self.font_size_spin.setGeometry(140, 340, 60, 32)
        self.font_size_spin.setRange(8, 24)
        self.font_size_spin.setValue(10)
        self.font_size_spin.show()
        
        # Apply font settings button
        self.apply_font_button = QPushButton("Apply Font Settings", self.ui.Settings)
        self.apply_font_button.setGeometry(40, 380, 150, 32)
        self.apply_font_button.clicked.connect(self.save_font_settings)
        self.apply_font_button.show()
        
        # Load current font settings if available
        font_family, font_size = self.db.get_font_settings()
        index = self.font_family_combo.findText(font_family)
        if index >= 0:
            self.font_family_combo.setCurrentIndex(index)
        self.font_size_spin.setValue(font_size)
    
    def save_api_key(self):
        """Save the OpenAI API key to the database"""
        api_key = self.ui.apifield.text().strip()
        if not api_key:
            QMessageBox.warning(self, "Warning", "Please enter an API key.")
            return
        
        # Save to database
        if self.db.save_api_key(api_key):
            self.openai_api.set_api_key(api_key)
            QMessageBox.information(self, "Success", "API key saved successfully.")
        else:
            QMessageBox.critical(self, "Error", "Failed to save API key.")
    
    def save_model(self, model):
        """Save the selected model to the database"""
        if not model:
            return
        
        # Save to database
        if self.db.save_model(model):
            self.openai_api.set_model(model)
            QMessageBox.information(self, "Success", f"Model set to {model}")
        else:
            QMessageBox.critical(self, "Error", "Failed to save model selection.")
    
    def fetch_and_update_models(self):
        """Fetch available models from OpenAI API and update the model combo box"""
        # Show loading message
        self.model_combo.clear()
        self.model_combo.addItem("Fetching models...")
        
        # Fetch models from OpenAI API
        success, models = self.openai_api.fetch_available_models()
        
        # Update model combo box
        self.model_combo.clear()
        if success:
            # Filter out models with specific keywords
            filtered_models = []
            excluded_keywords = ["instruct", "preview", "audio", "realtime", "search", "transcribe", "tts"]
            
            for model in models:
                # Check if any excluded keyword is in the model name
                if not any(keyword in model.lower() for keyword in excluded_keywords):
                    filtered_models.append(model)
            
            # Save filtered models to database
            self.db.save_models(filtered_models)
            
            self.model_combo.addItems(filtered_models)
            
            # Set current model from database
            current_model = self.db.get_model()
            index = self.model_combo.findText(current_model)
            if index >= 0:
                self.model_combo.setCurrentIndex(index)
            
            QMessageBox.information(self, "Success", f"Models fetched and saved successfully. Filtered out {len(models) - len(filtered_models)} models.")
        else:
            # Add default models if fetch fails
            default_models = ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo", "gpt-4o"]
            self.model_combo.addItems(default_models)
            QMessageBox.warning(self, "Warning", models[0])
    
    def load_prompt_file(self):
        """Load a prompt template from a file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Prompt Template File",
            "",
            "Text Files (*.txt);;All Files (*)"
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                
                # Get the file name without extension as the prompt name
                name = Path(file_path).stem
                
                # Save to database
                if self.db.save_prompt(name, content):
                    # Add to combo box if not already there
                    if self.ui.comboBox_prompt.findText(name) == -1:
                        self.ui.comboBox_prompt.addItem(name)
                    
                    # Select the newly added prompt
                    index = self.ui.comboBox_prompt.findText(name)
                    if index >= 0:
                        self.ui.comboBox_prompt.setCurrentIndex(index)
                    
                    QMessageBox.information(self, "Success", f"Prompt template '{name}' loaded successfully.")
                else:
                    QMessageBox.critical(self, "Error", "Failed to save prompt template.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load prompt file: {str(e)}")
    
    def save_font_settings(self):
        """Save font settings to the database"""
        font_family = self.font_family_combo.currentText()
        font_size = self.font_size_spin.value()
        
        # Save to database
        if self.db.save_font_settings(font_family, font_size):
            self.apply_font_settings()
            QMessageBox.information(self, "Success", "Font settings saved successfully.")
        else:
            QMessageBox.critical(self, "Error", "Failed to save font settings.")
    
    def apply_font_settings(self):
        """Apply the saved font settings to the UI"""
        font_family, font_size = self.db.get_font_settings()
        
        from PySide6.QtGui import QFont
        font = QFont(font_family, font_size)
        
        # Apply to text areas
        self.ui.Excerpts.setFont(font)
        self.ui.Rewrites.setFont(font)
        self.ui.analysis.setFont(font)
        self.ui.airesponse.setFont(font)
    
    def import_csv(self):
        """Import excerpts from a CSV file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            "",
            "CSV Files (*.csv)"
        )
        
        if not file_path:
            return
        
        success, message = self.db.import_csv(file_path)
        if success:
            QMessageBox.information(self, "Success", message)
        else:
            QMessageBox.critical(self, "Error", message)
    
    def export_to_csv(self):
        """Export excerpts to a CSV file"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save CSV File",
            "",
            "CSV Files (*.csv)"
        )
        
        if not file_path:
            return
        
        # Add .csv extension if not present
        if not file_path.lower().endswith('.csv'):
            file_path += '.csv'
        
        success, message = self.db.export_to_csv(file_path)
        if success:
            QMessageBox.information(self, "Success", message)
        else:
            QMessageBox.critical(self, "Error", message)
    
    def export_to_json(self):
        """Export excerpts to a JSON file"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save JSON File",
            "",
            "JSON Files (*.json)"
        )
        
        if not file_path:
            return
        
        # Add .json extension if not present
        if not file_path.lower().endswith('.json'):
            file_path += '.json'
        
        success, message = self.db.export_to_json(file_path)
        if success:
            QMessageBox.information(self, "Success", message)
        else:
            QMessageBox.critical(self, "Error", message)
    
    def clear_database(self):
        """Clear all excerpts from the database"""
        # Show confirmation dialog
        reply = QMessageBox.question(
            self,
            "Confirm Clear Database",
            "Are you sure you want to clear all excerpts from the database? This action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success, message = self.db.clear_database()
            if success:
                QMessageBox.information(self, "Success", message)
                # Reset current excerpt ID
                self.current_excerpt_id = None
                # Clear text fields
                self.ui.Excerpts.clear()
                self.ui.analysis.clear()
                self.ui.Rewrites.clear()
                self.ui.airesponse.clear()
            else:
                QMessageBox.critical(self, "Error", message)
    
    def setup_navigation_buttons(self):
        """Set up navigation buttons for excerpts"""
        # Previous excerpt button
        self.prev_button = QPushButton("Previous", self.ui.WorkArea)
        self.prev_button.setGeometry(120, 10, 100, 32)
        self.prev_button.clicked.connect(self.load_previous_excerpt)
        self.prev_button.show()
        
        # Next excerpt button
        self.next_button = QPushButton("Next", self.ui.WorkArea)
        self.next_button.setGeometry(230, 10, 100, 32)
        self.next_button.clicked.connect(self.load_next_excerpt)
        self.next_button.show()
    
    def load_random_excerpt(self):
        """Load a random excerpt from the database"""
        excerpt = self.db.get_random_excerpt()
        if not excerpt:
            QMessageBox.warning(self, "Warning", "No excerpts found in the database. Please import a CSV file first.")
            return
        
        # excerpt format: (id, excerpt, analysis, rewrite)
        self.current_excerpt_id = excerpt[0]
        self.ui.Excerpts.setText(excerpt[1])
        self.ui.analysis.setText(excerpt[2] if excerpt[2] else "")
        self.ui.Rewrites.setText(excerpt[3] if excerpt[3] else "")
        self.ui.airesponse.clear()
    
    def load_previous_excerpt(self):
        """Load the previous excerpt from the database"""
        if not self.current_excerpt_id:
            # If no current excerpt, load the first one
            excerpt = self.db.get_first_excerpt()
            if not excerpt:
                QMessageBox.warning(self, "Warning", "No excerpts found in the database. Please import a CSV file first.")
                return
        else:
            excerpt = self.db.get_previous_excerpt(self.current_excerpt_id)
            if not excerpt:
                QMessageBox.warning(self, "Warning", "No previous excerpt found.")
                return
        
        # excerpt format: (id, excerpt, analysis, rewrite)
        self.current_excerpt_id = excerpt[0]
        self.ui.Excerpts.setText(excerpt[1])
        self.ui.analysis.setText(excerpt[2] if excerpt[2] else "")
        self.ui.Rewrites.setText(excerpt[3] if excerpt[3] else "")
        self.ui.airesponse.clear()
    
    def load_next_excerpt(self):
        """Load the next excerpt from the database"""
        if not self.current_excerpt_id:
            # If no current excerpt, load the first one
            excerpt = self.db.get_first_excerpt()
            if not excerpt:
                QMessageBox.warning(self, "Warning", "No excerpts found in the database. Please import a CSV file first.")
                return
        else:
            excerpt = self.db.get_next_excerpt(self.current_excerpt_id)
            if not excerpt:
                QMessageBox.warning(self, "Warning", "No next excerpt found.")
                return
        
        # excerpt format: (id, excerpt, analysis, rewrite)
        self.current_excerpt_id = excerpt[0]
        self.ui.Excerpts.setText(excerpt[1])
        self.ui.analysis.setText(excerpt[2] if excerpt[2] else "")
        self.ui.Rewrites.setText(excerpt[3] if excerpt[3] else "")
        self.ui.airesponse.clear()
    
    def setup_markdown_viewer(self):
        """Set up the QTextBrowser for markdown rendering"""
        # Create a QTextBrowser to replace the QTextEdit for AI response
        self.markdown_viewer = QTextBrowser(self.ui.WorkArea)
        self.markdown_viewer.setGeometry(self.ui.airesponse.geometry())
        self.markdown_viewer.setOpenExternalLinks(True)  # Allow opening links
        self.markdown_viewer.anchorClicked.connect(lambda url: QDesktopServices.openUrl(url))
        
        # Hide the original QTextEdit
        self.ui.airesponse.hide()
        
        # Store a reference to the original QTextEdit for compatibility
        self.original_airesponse = self.ui.airesponse
        
        # Replace the reference in the UI
        self.ui.airesponse = self.markdown_viewer
        self.markdown_viewer.show()
    
    def send_to_openai(self):
        """Send the excerpt and rewrite to OpenAI for analysis"""
        if not self.current_excerpt_id:
            QMessageBox.warning(self, "Warning", "Please load an excerpt first.")
            return
        
        excerpt = self.ui.Excerpts.toPlainText().strip()
        rewrite = self.ui.Rewrites.toPlainText().strip()
        
        if not excerpt or not rewrite:
            QMessageBox.warning(self, "Warning", "Both excerpt and rewrite must not be empty.")
            return
        
        # Get selected prompt template
        prompt_name = self.ui.comboBox_prompt.currentText()
        prompt_template = ""
        
        # Check if it's a default template
        default_templates = self.openai_api.get_default_prompt_templates()
        if prompt_name in default_templates:
            prompt_template = default_templates[prompt_name]
        else:
            # Get from database
            saved_prompts = self.db.get_all_prompts()
            for prompt in saved_prompts:
                if prompt[1] == prompt_name:  # prompt[1] is the name
                    prompt_template = prompt[2]  # prompt[2] is the content
                    break
        
        if not prompt_template:
            prompt_template = default_templates["Basic Analysis"]  # Fallback to basic analysis
        
        # Send to OpenAI
        self.ui.airesponse.setHtml("<p>Analyzing...</p>")
        success, response = self.openai_api.analyze_rewrite(excerpt, rewrite, prompt_template)
        
        if success:
            # Convert markdown to HTML for display
            try:
                from markdown import markdown
                html_content = markdown(response)
                self.ui.airesponse.setHtml(html_content)
            except ImportError:
                # Fallback if markdown module is not available
                self.ui.airesponse.setHtml(f"<pre>{response}</pre>")
            
            # Save the rewrite to the database
            self.db.update_rewrite(self.current_excerpt_id, rewrite)
        else:
            self.ui.airesponse.setHtml(f"<p style='color:red'>Error: {response}</p>")


    def clear_prompts(self):
        """Clear all custom prompts from the database and combo box"""
        # Show confirmation dialog
        reply = QMessageBox.question(
            self,
            "Confirm Clear Prompts",
            "Are you sure you want to clear all custom prompt templates? Default templates will remain.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Clear prompts from database
            success, message = self.db.clear_prompts()
            
            if success:
                # Reset combo box to only show default templates
                self.ui.comboBox_prompt.clear()
                
                # Add default templates back
                default_templates = self.openai_api.get_default_prompt_templates()
                for name in default_templates.keys():
                    self.ui.comboBox_prompt.addItem(name)
                
                QMessageBox.information(self, "Success", "Custom prompt templates cleared successfully.")
            else:
                QMessageBox.critical(self, "Error", f"Failed to clear prompt templates: {message}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
