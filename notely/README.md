# Notely - AI-Powered Note Taking Application

A Django-based web application that allows users to create, edit, and manage notes with AI-powered automatic summarization using the T5 transformer model.

## Features

- **Create Notes**: Add new notes with titles and content
- **AI Summarization**: Automatically generates summaries for notes using the T5-small transformer model
- **Edit Notes**: Update existing notes with automatic re-summarization
- **Delete Notes**: Remove notes from the system
- **Chronological Display**: Notes are displayed in reverse chronological order (newest first)

## Technology Stack

### Core Framework
- **Django 5.2.4** - Web framework
- **asgiref 3.9.1** - ASGI server reference implementation
- **sqlparse 0.5.3** - SQL parsing for Django

### AI/ML Stack
- **transformers 4.53.2** - Hugging Face transformers library
- **torch 2.2.2** - PyTorch deep learning framework
- **torchaudio 2.2.2** - Audio processing for PyTorch
- **torchvision 0.17.2** - Computer vision for PyTorch
- **tokenizers 0.21.2** - Fast tokenizers for transformers
- **safetensors 0.5.3** - Safe tensor serialization
- **huggingface-hub 0.33.4** - Hugging Face model hub integration
- **hf-xet 1.1.5** - Hugging Face XET support
- **T5-small model** - Lightweight transformer for text summarization

### Scientific Computing
- **numpy 1.26.4** - Numerical computing
- **sympy 1.14.0** - Symbolic mathematics
- **mpmath 1.3.0** - Arbitrary-precision arithmetic

### HTTP & Networking
- **requests 2.32.4** - HTTP library
- **urllib3 2.5.0** - HTTP client
- **certifi 2025.7.9** - SSL certificates
- **charset-normalizer 3.4.2** - Character encoding detection
- **idna 3.10** - Internationalized domain names

### Utilities
- **regex 2024.11.6** - Regular expressions
- **tqdm 4.67.1** - Progress bars
- **filelock 3.18.0** - File locking
- **fsspec 2025.5.1** - Filesystem spec
- **networkx 3.4.2** - Network/graph algorithms
- **packaging 25.0** - Package version handling
- **typing_extensions 4.14.1** - Typing backports
- **Jinja2 3.1.6** - Template engine
- **MarkupSafe 3.0.2** - Safe string handling
- **PyYAML 6.0.2** - YAML parser
- **pillow 11.3.0** - Image processing

### Database
- **SQLite** (default Django database)

## Project Structure

```
notely/
├── manage.py                 # Django management script
├── notely/                   # Main project directory
│   ├── __init__.py
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   ├── asgi.py              # ASGI configuration
│   └── wsgi.py              # WSGI configuration
└── notes/                    # Notes application
    ├── __init__.py
    ├── admin.py             # Django admin configuration
    ├── apps.py              # App configuration
    ├── models.py            # Note model definition
    ├── views.py             # View functions
    ├── forms.py             # NoteForm for creating/editing notes
    ├── urls.py              # URL routing for notes app
    ├── utils.py             # AI summarization utility
    ├── templates/           # HTML templates
    └── migrations/          # Database migrations
```

## Installation

### Prerequisites

- Python 3.8 or higher (tested with Python 3.10-3.13)
- pip (Python package installer)
- Approximately 500MB of free disk space (for ML models and dependencies)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd notely
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv

   # On macOS/Linux:
   source venv/bin/activate

   # On Windows:
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   This will install all 30 required packages including:
   - Django and its dependencies
   - PyTorch and AI/ML libraries (transformers, tokenizers, etc.)
   - Scientific computing packages (numpy, sympy)
   - HTTP libraries and utilities

   Note: Installation may take several minutes due to the size of PyTorch and AI libraries.

4. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser** (optional, for admin access)
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Open your browser and navigate to `http://127.0.0.1:8000/`
   - Admin panel: `http://127.0.0.1:8000/admin/`

## Usage

### Creating a Note
1. Navigate to the home page
2. Click on "Add Note" or navigate to `/add-note/`
3. Enter a title and content
4. Click "Save" - the AI will automatically generate a summary

### Editing a Note
1. From the home page, click "Edit" on the desired note
2. Modify the title or content
3. Click "Save" - a new summary will be generated

### Deleting a Note
1. From the home page, click "Delete" on the desired note
2. The note will be removed from the system

## AI Summarization

The application uses the T5-small model from Hugging Face for text summarization:

- **Model**: t5-small (lightweight transformer model)
- **Minimum Text Length**: 30 words (shorter texts are returned as-is)
- **Input Limit**: First 512 characters of the note content
- **Summary Length**: 20-60 words
- **First Load**: The model downloads on first use (approximately 200MB)
- **Fallback Mode**: If the model cannot load (e.g., memory constraints on free hosting), the app automatically falls back to simple text truncation

### Memory Requirements

- **Local Development**: AI summarization works with sufficient RAM (2GB+)
- **Render Free Tier**: May fall back to simple summarization due to 512MB RAM limit
- **Render Paid Plans**: Full AI summarization available with 1GB+ RAM plans

## Database Schema

### Note Model
- `id`: Primary key (auto-generated)
- `title`: CharField (max 255 characters)
- `content`: TextField (unlimited length)
- `summary`: TextField (AI-generated, nullable)
- `created_at`: DateTimeField (auto-generated timestamp)

## Configuration

### Settings
Key configuration in [notely/settings.py](notely/settings.py):

- `DEBUG = True`: Set to `False` in production
- `SECRET_KEY`: Change this in production
- `ALLOWED_HOSTS`: Configure for deployment
- `DATABASES`: Uses SQLite by default (can be changed to PostgreSQL, MySQL, etc.)

## Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Accessing Django Shell
```bash
python manage.py shell
```

## Security Considerations

- The current `SECRET_KEY` in [notely/settings.py](notely/settings.py#L23) is for development only
- `DEBUG` mode is enabled - disable in production
- Configure `ALLOWED_HOSTS` before deploying
- Consider using environment variables for sensitive settings

## Performance Notes

- The T5 model loads into memory on first summarization request
- Model remains cached in memory for subsequent requests
- Initial summarization may take a few seconds; subsequent requests are faster
- Text is truncated to 512 characters before summarization to ensure model compatibility

## Troubleshooting

### Model Download Issues
If the T5 model fails to download:
- Check your internet connection
- Ensure you have sufficient disk space (approximately 200MB)
- The model will download to the Hugging Face cache directory

### Long Load Times
- First summarization request downloads the model (one-time operation)
- Server restart requires model reload
- Consider pre-loading the model in production environments

## Future Enhancements

Potential features for future development:
- User authentication and authorization
- Note categories/tags
- Search functionality
- Export notes to PDF/Markdown
- Rich text editor
- Note sharing capabilities
- Multiple AI models for summarization

## License

This project is provided as-is for educational and development purposes.

## Contributing

Contributions are welcome. Please ensure all tests pass before submitting pull requests.

## Support

For issues, questions, or contributions, please open an issue in the repository.
