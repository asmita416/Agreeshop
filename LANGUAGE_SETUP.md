# Multi-Language Support Implementation Guide

## Overview
This document explains how the multi-language feature works in your AgriShop application and how to maintain/extend it.

## How It Works

### 1. **Translation System Architecture**
- **Supported Languages**: English (en), Hindi (hi), Marathi (mr)
- **Storage**: Translation files in `/translations/` folder as JSON files
- **Session-based**: Language preference is stored in Flask session
- **Fallback**: Defaults to English if translation key not found

### 2. **Translation Files** (`/translations/`)
```
translations/
├── en.json   (English)
├── hi.json   (Hindi)
└── mr.json   (Marathi)
```

Each JSON file contains key-value pairs:
```json
{
  "home": "Home",
  "categories": "Categories",
  "add_to_cart": "Add to Cart"
}
```

### 3. **Backend Implementation** (app.py)

**Key Functions:**
- `load_translations()` - Loads all translation files on app startup
- `get_locale()` - Gets current language from session (defaults to 'en')
- `get_translation(key, default='')` - Returns translated string for a key
- `set_language(language)` - Route to change language

**Language Switching Route:**
```
/set_language/<language>
```
Examples:
- `/set_language/en` - Switch to English
- `/set_language/hi` - Switch to Hindi
- `/set_language/mr` - Switch to Marathi

### 4. **Frontend Template Usage** (Templates)

In any template, use the translation function:

```html
<!-- Single translation -->
<a href="/">{{ request.get_translation('home') }}</a>

<!-- With default fallback -->
<p>{{ request.get_translation('custom_key', 'Default English Text') }}</p>

<!-- In text content -->
<h1>{{ request.get_translation('welcome_to_agrishop') }}</h1>
```

**Language Selector** (added to base.html navbar):
```html
<li class="nav-item dropdown">
    <a class="nav-link dropdown-toggle" href="#" id="languageDropdown">
        <i class="bi bi-globe"></i> Language
    </a>
    <ul class="dropdown-menu">
        <li><a href="/set_language/en">🇬🇧 English</a></li>
        <li><a href="/set_language/hi">🇮🇳 Hindi</a></li>
        <li><a href="/set_language/mr">🇮🇳 Marathi</a></li>
    </ul>
</li>
```

## How to Add/Update Translations

### Step 1: Add new translation keys to JSON files

Edit all three files: `en.json`, `hi.json`, `mr.json`

**en.json:**
```json
{
  "new_feature": "New Feature",
  "existing_key": "value"
}
```

**hi.json:**
```json
{
  "new_feature": "नई सुविधा",
  "existing_key": "मूल्य"
}
```

**mr.json:**
```json
{
  "new_feature": "नवीन वैशिष्ट्य",
  "existing_key": "मूल्य"
}
```

### Step 2: Use in templates

```html
<button>{{ request.get_translation('new_feature') }}</button>
```

## Current Translations Included

- Navigation menu items (Home, Categories, Cart, etc.)
- Product page buttons (Add to Cart, View All, etc.)
- Product categories (Seeds, Fertilizers, Pesticides, Tools, Machinery)
- User menu items (Profile, My Orders, Logout, etc.)
- Cart and Wishlist labels
- Form labels (Email, Password, Phone, Address, etc.)
- Footer text
- Status badges (Stock, Out of Stock, etc.)

## Extending to More Languages

### To add a new language (e.g., Gujarati - 'gu'):

1. **Add to supported languages** in app.py:
```python
SUPPORTED_LANGUAGES = ['en', 'hi', 'mr', 'gu']
```

2. **Create new translation file** `translations/gu.json` with all keys

3. **Add to language selector** in base.html navbar:
```html
<li><a class="dropdown-item" href="/set_language/gu">🇮🇳 Gujarati</a></li>
```

## Best Practices

1. **Keep keys consistent** - Use underscore_case for JSON keys
2. **Translate at display time** - Use `request.get_translation()` in templates
3. **Provide fallback values** - Pass default text to `get_translation()` for optional strings
4. **Test all languages** - Switch language and verify all UI elements display correctly
5. **User experience** - Show language selector prominently (navbar dropdown)
6. **Session persistence** - Language preference is kept in Flask session throughout the user's visit

## Testing the Feature

1. **Switch Language**: Click on Language dropdown in navbar → Select Hindi/Marathi/English
2. **Verify**: All text should change to the selected language
3. **Check All Pages**: Home, Categories, Cart, Login, Profile, etc.
4. **Browser Back/Forward**: Language preference is maintained in session

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Translation not showing | Check key exists in JSON file and spelled correctly |
| All text in English | Language not set in session, user has never clicked language selector |
| Only some text translated | Some templates may not be updated yet with translation calls |
| New language not appearing | Added to SUPPORTED_LANGUAGES and created JSON file? |

## Files Modified/Created

- **Created**: `/translations/en.json`, `/translations/hi.json`, `/translations/mr.json`
- **Modified**: `app.py` (added language functions and routes)
- **Modified**: `templates/base.html` (added language selector, updated text)
- **Modified**: `templates/index.html` (updated to use translations)

## Next Steps (Optional Enhancements)

1. **Database Storage**: Store language preference in user profile for logged-in users
2. **Browser Language Detection**: Auto-detect browser language on first visit
3. **More Languages**: Add more regional languages (Gujarati, Punjabi, etc.)
4. **Translation Management**: Create admin panel to manage translations without file editing
5. **i18n Formatting**: Use `Babel` or `gettext` for more advanced localization (dates, numbers, currencies)

---

**Version**: 1.0  
**Last Updated**: 2024
