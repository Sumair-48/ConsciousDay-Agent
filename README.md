# ConsciousDay Agent 🌅

*Reflect inward. Act with clarity.*

A journaling-based AI assistant that reads your morning inputs and provides emotional insights and daily strategy recommendations. Built with Streamlit, LangChain, and OpenRouter API.

Link: https://conscious-dayagent.streamlit.app/

## 🌟 Features

### Core Functionality
- **📝 Morning Reflection Form**: Capture journal entries, dreams, intentions, and priorities
- **🤖 AI-Powered Analysis**: Get personalized emotional insights and mindset analysis
- **🎯 Strategic Planning**: Receive tailored daily strategies based on your inputs
- **💾 Persistent Storage**: All entries saved securely in SQLite database
- **📚 Historical View**: Browse and reflect on past journal entries
- **🔐 User Authentication**: Secure login system to protect your personal data

### AI Insights Provided
- **Inner Reflection Summary**: Analysis of your emotional and mental state
- **Dream Interpretation**: Meaningful interpretation of your dreams
- **Energy/Mindset Insight**: Understanding of your current mental framework
- **Suggested Day Strategy**: Time-aligned tasks and mindset recommendations

## 🚀 Quick Start

### 1. Clone & Install
```bash
git clone https://github.com/yourusername/consciousday-agent.git
cd consciousday-agent
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env and add your OpenRouter API key
echo "OPENROUTER_API_KEY=your_api_key_here" >> .env
```

### 3. Run the Application
```bash
streamlit run app.py
```

### 4. Access & Login
- Open: `http://localhost:8501`
- **Demo Credentials:**
  - Username: `demo_user`
  - Password: `demo123`

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Frontend** | Streamlit |
| **AI Framework** | LangChain |
| **AI API** | OpenRouter (supports Claude, GPT, Gemini, etc.) |
| **Database** | SQLite |
| **Authentication** | Streamlit Authenticator + bcrypt |
| **Testing** | unittest |

## 📁 Project Structure

```
consciousday_agent/
├── 📄 app.py                    # Main Streamlit application
├── 📋 requirements.txt          # Dependencies
├── 🔧 config/
│   └── settings.py             # Configuration settings
├── 🧩 components/
│   ├── auth.py                 # Authentication system
│   ├── forms.py                # Form components
│   └── display.py              # Display components
├── 🤖 agent/
│   ├── langchain_agent.py      # AI agent logic
│   └── prompts.py              # Prompt templates
├── 🗄️ database/
│   ├── db_manager.py           # Database operations
│   └── models.py               # Data models
├── 📖 pages/
│   ├── home.py                 # Main journaling page
│   └── history.py              # Historical entries
├── 🛠️ utils/
│   └── helpers.py              # Utility functions
└── 🧪 tests/
    ├── test_db.py              # Database tests
    └── test_agent.py           # Agent tests
```

## 🎮 Usage Guide

### Daily Reflection Workflow

1. **🌅 Morning Setup**
   - Login to your account
   - Navigate to "Daily Reflection"

2. **📝 Fill Your Reflection**
   - **Morning Journal**: Free-form thoughts and feelings
   - **Intention**: Your guiding principle for the day
   - **Dream**: Any dreams you remember (optional)
   - **Top 3 Priorities**: Your most important tasks

3. **✨ Get AI Insights**
   - Click "Generate Reflection & Strategy"
   - Review your personalized analysis in 4 tabs:
     - 🪞 Inner Reflection
     - 🌙 Dream Insights
     - 🧠 Mindset Analysis
     - 🎯 Day Strategy

4. **📚 Track Your Journey**
   - Visit "Journal History" to review past entries
   - Monitor your growth and patterns over time

### Sample Entry

**Morning Journal**: "Feeling a bit anxious about the presentation today, but also excited about the new project starting. Had trouble sleeping but feel energized now."

**Intention**: "Stay calm and confident while being open to new opportunities"

**Dream**: "Dreamed I was flying over a city, felt very free and powerful"

**Priorities**: 
1. Prepare and deliver presentation
2. Review new project requirements  
3. Team check-in meeting

## ⚙️ Configuration

### Environment Variables

Create a `.env` file with:

```env
# Required: OpenRouter API key for AI functionality
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Optional: Custom authentication cookie key
AUTH_COOKIE_KEY=your_secret_cookie_key_here

# Optional: Custom database path (defaults to entries.db)
DATABASE_PATH=entries.db
```

### API Setup

1. **Get OpenRouter API Key**:
   - Visit [OpenRouter.ai](https://openrouter.ai/)
   - Create account and get API key
   - Add to `.env` file

2. **Model Configuration**:
   - Default: `anthropic/claude-3-haiku` (fast & cost-effective)
   - Customizable in `config/settings.py`

### Database

- **Type**: SQLite (file-based, no setup required)
- **Location**: `entries.db` (created automatically)
- **Schema**: Includes entries table with user data and AI responses

## 🧪 Testing

Run the complete test suite:

```bash
# Run all tests
python -m pytest tests/

# Run specific test files
python -m unittest tests.test_db
python -m unittest tests.test_agent

# Run with coverage
python -m pytest tests/ --cov=.
```

### Test Coverage

- ✅ Database operations (CRUD)
- ✅ AI agent functionality  
- ✅ Response parsing
- ✅ Error handling
- ✅ Data validation

## 🌐 Deployment

### Streamlit Cloud (Recommended)

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**:
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Add environment variables in settings
   - Deploy!

3. **Environment Variables in Streamlit Cloud**:
   - `OPENROUTER_API_KEY`: Your API key
   - `AUTH_COOKIE_KEY`: Random secret string

### Local Production

```bash
# Install production dependencies
pip install -r requirements.txt

# Run with production settings
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

### Docker (Optional)

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## 🔧 Development

### Adding New Features

1. **Create Feature Branch**:
   ```bash
   git checkout -b feature/new-feature
   ```

2. **Follow Structure**:
   - UI components → `components/`
   - Pages → `pages/`
   - Business logic → `agent/` or `utils/`
   - Tests → `tests/`

3. **Add Tests**:
   ```python
   # tests/test_new_feature.py
   import unittest
   from your_module import YourClass
   
   class TestNewFeature(unittest.TestCase):
       def test_functionality(self):
           # Your test code
           pass
   ```

### Code Style

- **Python**: Follow PEP 8
- **Comments**: Document complex logic
- **Type Hints**: Use where helpful
- **Error Handling**: Always include try/catch blocks

## 🐛 Troubleshooting

### Common Issues

**1. API Key Not Working**
```bash
# Check your .env file
cat .env | grep OPENROUTER_API_KEY

# Verify API key format
# Should start with "sk-or-v1-"
```

**2. Database Issues**
```bash
# Delete and recreate database
rm entries.db
python -c "from database.db_manager import DatabaseManager; DatabaseManager()"
```

**3. Authentication Problems**
```bash
# Clear session state
# Delete browser cookies or use incognito mode
```

**4. Module Import Errors**
```bash
# Ensure you're in the project root
pwd
# Should end with /consciousday-agent

# Check Python path
export PYTHONPATH="${PYTHONPATH}:."
```

### Debug Mode

Enable debug logging:

```python
# In app.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Performance Issues

- **Slow AI responses**: Try different model in `config/settings.py`
- **UI lag**: Clear browser cache and session state
- **Database slow**: Check `entries.db` file size

## 📊 Features Checklist

### ✅ Core Requirements (All Implemented)
- [x] Form with 4 user inputs
- [x] LangChain agent response  
- [x] Reflection + Strategy output
- [x] Save entries in SQLite
- [x] View previous entries by date
- [x] Clean UI (Streamlit)
- [x] Code clarity and documentation
- [x] Deployed and working

### ✅ Bonus Features (All Implemented)
- [x] Streamlit Auth to protect journal data
- [x] Session State to avoid re-running
- [x] Clean modular structure with folders
- [x] Error handling for agent/API responses  
- [x] Simple tests for DB operations

### 🚀 Additional Enhancements
- [x] Fallback responses when API unavailable
- [x] Input validation and sanitization  
- [x] Rich UI with tabs and metrics
- [x] Comprehensive logging system
- [x] Professional styling and UX
- [x] Complete documentation

## 🤝 Contributing

1. **Fork the Repository**
2. **Create Feature Branch**: `git checkout -b feature/amazing-feature`
3. **Make Changes**: Follow the project structure and style
4. **Add Tests**: Ensure your code is tested
5. **Commit Changes**: `git commit -m 'Add amazing feature'`
6. **Push to Branch**: `git push origin feature/amazing-feature`
7. **Open Pull Request**: Describe your changes

### Contribution Guidelines

- **Code Quality**: Write clean, documented code
- **Testing**: Add tests for new functionality
- **Documentation**: Update README and docstrings
- **Compatibility**: Ensure changes work with existing features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Streamlit Team**: For the amazing web framework
- **LangChain**: For the AI agent framework  
- **OpenRouter**: For providing access to multiple AI models
- **Open Source Community**: For the tools and libraries used

## 📞 Support

### Getting Help

1. **Documentation**: Check this README and code comments
2. **Issues**: Search existing GitHub issues
3. **New Issue**: Create detailed bug report or feature request
4. **Discussions**: Use GitHub Discussions for questions

---

**Built with ❤️ for mindful daily reflection and intentional living.**

*Start your conscious day journey today!* 🌅✨
