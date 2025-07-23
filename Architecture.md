# Multilingual Streamlit Application Architecture

## Project Overview
A multilingual web application built with Streamlit for Netanya Municipality, featuring Hebrew (RTL) as default language, English (LTR), French (LTR), and Russian (LTR) support. The application manages user interactions for category selection, street number selection, and data submission with persistent local storage, advanced URL parameter handling, and enhanced user experience features.

## Technology Stack
- **Frontend**: Streamlit (Python)
- **Database**: Supabase (PostgreSQL)
- **Storage**: Supabase Storage
- **Local Storage**: Browser localStorage for user data persistence
- **HTTP Client**: Requests library for API calls
- **Validation**: Israeli phone number validation
- **Notifications**: Toast-style success notifications

## Database Schema

### Table 1: Categories
```sql
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    text TEXT NOT NULL, -- Comma-separated array of text options
    image_url VARCHAR(500) NOT NULL,
    event_call_desc VARCHAR(255) NOT NULL -- For API submission
);
```

### Table 2: Street Numbers
```sql
CREATE TABLE street_numbers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    image_url VARCHAR(500) NOT NULL,
    house_number VARCHAR(50) NOT NULL -- For API submission
);
```

## Application Structure

### Core Components

#### 1. Enhanced Header Component
- **Language Selector**: Icons for Hebrew (default), English, French, Russian
- **Banner Image**: PNG banner placeholder
- **Auto-Clearing Search Box**: Real-time local filtering that clears automatically on navigation
- **Language Persistence**: Selected language stored in localStorage (defaults to Hebrew)

#### 2. Advanced Navigation System
- **Page 1**: Categories Grid View
- **Page 2**: Street Numbers Grid View  
- **Page 3**: Summary Page with Editable Text Field
- **URL Parameter Support**: Direct navigation via `?category={id}&street={id}`
- **State Management**: Session state for current page and selections
- **Auto-Clear Search**: Search query clears on every navigation step

#### 3. Enhanced User Data Management
- **Local Storage Keys**:
  - `user_first_name`: User's first name (max 35 chars)
  - `user_last_name`: User's last name (max 35 chars)
  - `user_id`: User's ID (max 12 digits, numbers only, optional)
  - `user_phone`: User's phone (Israeli format validation)
  - `user_email`: User's email address (optional)
  - `selected_language`: Current language preference (defaults to Hebrew)
  - `ticket_history`: Array of submitted ticket numbers
- **Auto-complete**: Browser-native autocomplete for form fields
- **Enhanced Validation**: Israeli phone number validation with specific patterns
- **Random Data Generation**: Pre-filled Hebrew names for development/testing

## Advanced User Flows

### URL Parameter Flow
1. **Direct Navigation**: User visits URL with `?category={id}&street={id}` parameters
2. **Parameter Processing**: Application processes parameters and clears them from URL
3. **User Data Check**: If user data exists, navigate directly to summary page
4. **Data Collection**: If no user data, show popup first then proceed to summary
5. **Category Only**: If only `?category={id}`, navigate to street numbers page

### Enhanced New User Flow
1. **Categories Page**: User sees grid of category boxes with auto-clearing search
2. **Category Selection**: Click triggers mandatory data popup with pre-filled Hebrew data
3. **Enhanced Data Collection Popup**:
   - First Name field (text, max 35 chars, pre-filled with Hebrew name)
   - Last Name field (text, max 35 chars, pre-filled with Hebrew name)
   - ID field (numbers only, max 12 digits, optional)
   - Phone field (Israeli validation, required)
   - Email field (valid email format, optional, pre-filled)
   - "Save Locally" message displayed
   - Exit option returns to categories page
4. **Data Persistence**: User data saved to localStorage
5. **Street Numbers Page**: Grid view with auto-clearing search
6. **Summary Page**: Display all data with editable text field and SEND button
7. **HTTP POST Request**: Submit multipart/form-data to Netanya Municipality API
8. **Success Notification**: Toast notification with ticket number
9. **Ticket History**: Save ticket number to local history
10. **Flow Restart**: Return to categories page

### Enhanced Existing User Flow
1. **Categories Page**: User sees grid with auto-clearing search
2. **Category Selection**: Direct navigation to street numbers (search clears)
3. **Street Numbers Page**: Grid view with auto-clearing search
4. **Summary Page**: Display data with editable text field and SEND button
5. **HTTP POST Request**: Submit to API
6. **Toast Success Notification**: Display success message with ticket number
7. **Flow Restart**: Return to categories page

## Enhanced UI/UX Specifications

### URL Parameter System
- **Parameter Format**: `?category={id}&street={id}`
- **Parameter Processing**: Single-pass processing with automatic URL cleaning
- **Deep Linking**: Direct navigation to summary page if user data exists
- **Fallback Handling**: Graceful handling of invalid parameters

### Auto-Clearing Search Functionality
- **Trigger Points**: Search clears on category selection, street selection, and page navigation
- **Real-time Filtering**: Local JavaScript filtering with 300ms debounce
- **Scope**: Current page content only
- **Multilingual**: Search works in all supported languages including Hebrew

### Enhanced Responsive Design
- **Desktop**: Dynamic grid layout (3-4 items per row)
- **Tablet**: 2-3 items per row with touch-friendly targets
- **Mobile**: 1-2 items per row with enhanced touch interactions
- **Breakpoints**: CSS media queries with mobile-first approach

### Enhanced Grid Components
- **Category Boxes**: Image + name display with hover effects
- **Street Number Boxes**: Image + name display with enhanced styling
- **Touch Interactions**: Minimum 44px touch targets
- **Loading States**: Placeholder content while data loads
- **No Results**: User-friendly "no results" message

### Advanced Popup Components
- **Success Toast**: Non-blocking toast notification with ticket number
- **Error Toast**: "Failed, please try again" with restart option
- **Enhanced Data Collection**: Pre-filled random Hebrew data for development
- **Validation Feedback**: Real-time Israeli phone number validation

## Enhanced Data Flow

### 1. Application Initialization with URL Parameters
```
Load environment variables → Initialize services → Process URL parameters → 
Load user data from localStorage → Set language preference (Hebrew default) → 
Load categories/streets from Supabase → Clear URL parameters → Render appropriate page
```

### 2. Enhanced Category Selection
```
User clicks category → Clear search query → Check if user data exists → 
Show popup (new) or continue (existing) → Process URL parameters if present
```

### 3. Enhanced Street Number Selection
```
Load street numbers from Supabase → Clear search query → User selects → 
Navigate to summary → Process URL parameters if present
```

### 4. Enhanced Data Submission
```
Prepare multipart/form-data payload → HTTP POST request to Netanya Municipality → 
Handle response → Show toast notification → Save ticket to history → 
Clear search → Restart flow to categories
```

## Enhanced HTTP API Integration

### Netanya Municipality API Specification

#### Request Details
- **URL**: `https://www.netanya.muni.il/_layouts/15/NetanyaMuni/incidents.ashx?method=CreateNewIncident`
- **Method**: POST
- **Content-Type**: `multipart/form-data`
- **Host**: `www.netanya.muni.il`

#### Enhanced Request Body Format
```json
{
  "eventCallSourceId": 4,
  "cityCode": "7400",
  "cityDesc": "נתניה",
  "eventCallCenterId": "3",
  "eventCallDesc": "category_event_call_desc",  // From selected category
  "streetCode": "898",
  "streetDesc": "קרל פופר",
  "houseNumber": "street_house_number",         // From selected street
  "callerFirstName": "user_first_name",         // User's first name
  "callerLastName": "user_last_name",           // User's last name
  "callerTZ": "user_id",                        // User's ID (optional)
  "callerPhone1": "user_phone",                 // User's phone (Israeli format)
  "callerEmail": "user_email",                  // User's email (optional)
  "contactUsType": "3"
}
```

#### Enhanced Response Handling
- **Success (200)**: Show toast notification with ticket number, save to history, restart flow
- **Error (4xx/5xx)**: Show error toast, restart flow
- **Network Error**: Show error toast with retry option

## Enhanced Internationalization (i18n)

### Language Support with Hebrew Default
- **Hebrew (he)**: RTL layout, Hebrew text, **DEFAULT LANGUAGE**
- **English (en)**: LTR layout, English text
- **French (fr)**: LTR layout, French text
- **Russian (ru)**: LTR layout, Russian text

### Enhanced Translation Keys
- All UI text elements including search placeholders
- Enhanced error messages for Israeli phone validation
- Success messages with ticket number formatting
- Form labels with Hebrew-specific help text
- Toast notification content

### Comprehensive RTL Support
- CSS direction property for Hebrew
- Text alignment adjustments for all form fields
- Icon positioning for RTL layout
- Grid layout optimization for RTL
- Search box RTL support

## Enhanced Security Considerations

### Enhanced Data Validation
- **Israeli Phone Validation**: Specific patterns for Israeli landline and mobile numbers
- **Client-side validation**: Real-time feedback for all form inputs
- **Input sanitization**: Prevent XSS with proper escaping
- **Email format validation**: Optional but validated when provided
- **ID validation**: Optional numeric-only validation

### Enhanced Local Storage Security
- **Selective persistence**: User data, language, and ticket history only
- **No sensitive data transmission**: Only final submission to municipality
- **Ticket history tracking**: Local storage of successful submissions
- **Data isolation**: No cross-site data leakage

## Enhanced Performance Optimization

### Advanced Data Loading
- **Smart caching**: Session state caching with selective updates
- **Lazy loading**: Progressive image loading for grid items
- **Debounced search**: 300ms delay for search input
- **URL parameter optimization**: Single-pass processing with efficient state updates

### Enhanced Search Performance
- **Auto-clearing mechanism**: Automatic search reset on navigation
- **Local filtering**: No server requests for search
- **Optimized algorithms**: Efficient string matching for multilingual content
- **Memory management**: Proper cleanup of search state

### API Performance Enhancements
- **Connection pooling**: Reuse HTTP connections
- **Timeout handling**: Configurable request timeouts
- **Retry logic**: Intelligent retry for failed requests
- **Response caching**: Cache successful submissions

## Enhanced Error Handling

### Comprehensive User Experience
- **Toast notifications**: Non-blocking error and success messages
- **Graceful degradation**: Fallback content for network issues
- **Clear error messages**: User-friendly messages in selected language
- **Recovery options**: Easy restart and retry mechanisms

### Technical Error Management
- **Comprehensive logging**: Error tracking for debugging
- **Fallback content**: Default content for failed data loads
- **Network resilience**: Timeout and retry mechanisms
- **URL parameter validation**: Handle invalid or malformed parameters

## Application Modes: Enhanced Debug and Release

### 1. Release Mode
- **Purpose**: Production use with real municipality API
- **Behavior**: All features live, real HTTP POST requests
- **Configuration**: `APP_MODE=release` or `DEBUG=False`
- **Validation**: Full Israeli phone number validation
- **Notifications**: Real toast notifications with actual ticket numbers

### 2. Enhanced Debug Mode
- **Purpose**: Development and testing with mock responses
- **Behavior**: Mock API responses, no real submissions
- **Configuration**: `APP_MODE=debug` or `DEBUG=True`
- **Features**: Pre-filled Hebrew random data for testing
- **Mock Response**: Simulated success with fake ticket numbers

#### Enhanced Mock Response Example
```json
{
  "ResultCode": 200,
  "ErrorDescription": "",
  "ResultStatus": "SUCCESS CREATE",
  "ResultData": {
    "incidentGuid": "mock-guid-1234",
    "incidentNumber": "MOCK-0001"
  },
  "data": "MOCK-0001"
}
```

## Enhanced Deployment and Configuration

### Environment Variables
- `APP_MODE`: `release` for production or `debug` for development
- `DEBUG`: Boolean flag for backward compatibility  
- `SUPABASE_URL` and `SUPABASE_KEY`: Database configuration
- `API_ENDPOINT`: Municipality API endpoint
- `DEFAULT_LANGUAGE`: Override default language (defaults to Hebrew)

### Enhanced API Service Logic
- **Debug mode**: Mock responses with random ticket numbers
- **Release mode**: Real municipality API integration
- **Validation**: Environment-specific validation rules
- **Logging**: Mode-appropriate logging levels

## Enhanced Testing Strategy

### Unit Tests
- Israeli phone number validation functions
- URL parameter processing utilities
- Data transformation and validation
- Hebrew text transliteration functions

### Integration Tests
- Supabase data loading with ID lookups
- HTTP API integration with mock/real modes
- Local storage operations including ticket history
- Multipart form data creation and submission

### User Acceptance Tests
- Complete user flows including URL parameter navigation
- Mobile responsiveness across all devices
- Multilingual functionality with Hebrew as default
- API submission scenarios in both debug and release modes

## Future Enhancements

### Potential Advanced Features
- **File Upload Support**: Ready infrastructure for future file attachments
- **Advanced Ticket History**: User interface for viewing past submissions
- **Push Notifications**: Real-time updates on ticket status
- **Offline Mode**: Service worker for offline form completion
- **Advanced Analytics**: User interaction tracking and analytics
- **Admin Panel**: Content management for categories and streets
- **API Response Caching**: Intelligent caching for improved performance

### Scalability Considerations
- **Database Optimization**: Indexing for performance at scale
- **CDN Integration**: Global content delivery for images
- **Caching Strategies**: Redis or similar for session management
- **Load Balancing**: API request distribution
- **Monitoring**: Real-time application monitoring and alerting

## Updated Implementation Notes (Current)

### Completed Features ✅
- **Hebrew Default Language**: Application starts in Hebrew with RTL support
- **URL Parameter Handling**: Full support for direct navigation via URL parameters
- **Auto-Clearing Search**: Search box clears automatically on every navigation
- **Israeli Phone Validation**: Specific validation patterns for Israeli phone numbers
- **Toast Notifications**: Success notifications with ticket numbers (replacing popup)
- **Random Hebrew Data**: Pre-filled development data with Hebrew names
- **Enhanced Mobile UX**: Touch-friendly design with improved interactions
- **Ticket History**: Local storage of successful submission ticket numbers
- **Debug/Release Modes**: Full mock API support for development

### Architecture Highlights
- **Editable Text Field**: Summary page includes editable text area for additional information
- **Multipart Form Data**: Structured for easy file upload addition in future
- **Local Storage Optimization**: Efficient data persistence with selective clearing
- **Comprehensive Error Handling**: Graceful degradation with user-friendly messages
- **Performance Optimized**: Debounced search, smart caching, efficient state management
- **Accessibility Ready**: WCAG-compliant design with proper ARIA labels
- **Production Ready**: Full configuration management for different deployment environments

This enhanced architecture document reflects the current state of the fully-featured multilingual Streamlit application with advanced URL parameter handling, Hebrew-first design, and comprehensive user experience optimizations. 