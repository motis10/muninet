# Multilingual Streamlit Application Architecture

## Project Overview
A multilingual web application built with Streamlit, featuring Hebrew (RTL), English (LTR), French (LTR), and Russian (LTR) support. The application manages user interactions for category selection, street number selection, and data submission with persistent local storage.

## Technology Stack
- **Frontend**: Streamlit (Python)
- **Database**: Supabase (PostgreSQL)
- **Storage**: Supabase Storage
- **Local Storage**: Browser localStorage for user data persistence
- **HTTP Client**: Requests library for API calls

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

#### 1. Header Component
- **Language Selector**: Icons for Hebrew, English, French, Russian
- **Banner Image**: PNG banner placeholder
- **Search Box**: Real-time local filtering for current page content
- **Language Persistence**: Selected language stored in localStorage

#### 2. Navigation System
- **Page 1**: Categories Grid View
- **Page 2**: Street Numbers Grid View  
- **Page 3**: Summary Page
- **State Management**: Session state for current page and selections

#### 3. User Data Management
- **Local Storage Keys**:
  - `user_first_name`: User's first name (max 35 chars)
  - `user_last_name`: User's last name (max 35 chars)
  - `user_id`: User's ID (max 12 digits, numbers only)
  - `user_phone`: User's phone (max 15 digits, numbers only)
  - `user_email`: User's email address
  - `selected_language`: Current language preference
- **Auto-complete**: Browser-native autocomplete for form fields
- **Validation**: Client-side validation with multilingual error messages

## User Flows

### New User Flow
1. **Categories Page**: User sees grid of category boxes
2. **Category Selection**: Click triggers mandatory data popup
3. **Data Collection Popup**:
   - First Name field (text, max 35 chars)
   - Last Name field (text, max 35 chars)
   - ID field (numbers only, max 12 digits)
   - Phone field (numbers only, max 15 digits)
   - Email field (valid email format)
   - "Save Locally" message displayed
   - Exit option returns to categories page
4. **Data Persistence**: User data saved to localStorage
5. **Street Numbers Page**: Grid view of street number boxes
6. **Summary Page**: Display all collected data with SEND button
7. **HTTP POST Request**: Submit data to Netanya Municipality API
8. **Success/Error Handling**: Popup with ticket number (success) or error message and restart option

### Existing User Flow
1. **Categories Page**: User sees grid of category boxes
2. **Category Selection**: Direct navigation to street numbers page (no popup)
3. **Street Numbers Page**: Grid view of street number boxes
4. **Summary Page**: Display all data with SEND button
5. **HTTP POST Request**: Submit data to Netanya Municipality API
6. **Success/Error Handling**: Popup with ticket number (success) or error message and restart option

## UI/UX Specifications

### Responsive Design
- **Desktop**: Dynamic grid layout (3-4 items per row)
- **Tablet**: 2-3 items per row
- **Mobile**: 1-2 items per row
- **Breakpoints**: CSS media queries for responsive behavior

### Grid Components
- **Category Boxes**: Image + name display
- **Street Number Boxes**: Image + name display
- **Hover Effects**: Visual feedback on interaction
- **Loading States**: Placeholder content while data loads

### Search Functionality
- **Real-time Filtering**: Local JavaScript filtering
- **Scope**: Current page content only
- **Case-insensitive**: Search across names and text content
- **Multilingual**: Search works in all supported languages

### Popup Components
- **Success Popup**: Display ticket number with "Start Over" button
- **Error Popup**: "Failed, please try again" button
- **Data Collection Popup**: Form with validation and exit option

## Data Flow

### 1. Application Initialization
```
Load user data from localStorage → Set language preference → Load categories from Supabase
```

### 2. Category Selection
```
User clicks category → Check if user data exists → Show popup (new) or continue (existing)
```

### 3. Street Number Selection
```
Load street numbers from Supabase → User selects → Navigate to summary
```

### 4. Data Submission
```
Prepare multipart/form-data payload → HTTP POST request to Netanya Municipality → Handle response → Show popup → Restart flow
```

## HTTP API Integration

### Netanya Municipality API Specification

#### Request Details
- **URL**: `https://www.netanya.muni.il/_layouts/15/NetanyaMuni/incidents.ashx?method=CreateNewIncident`
- **Method**: POST
- **Content-Type**: `multipart/form-data`
- **Host**: `www.netanya.muni.il`

#### Required Headers
```
Accept-Language: en-US,en;q=0.9
X-Requested-With: XMLHttpRequest
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36
Accept: application/json;odata=verbose
Origin: https://www.netanya.muni.il
Referer: https://www.netanya.muni.il/CityHall/ServicesInnovation/Pages/PublicComplaints.aspx
Accept-Encoding: gzip, deflate, br
```

#### Request Body Format (multipart/form-data)
```json
{
  "eventCallSourceId": 4,
  "cityCode": "7400",
  "cityDesc": "נתניה",
  "eventCallCenterId": "3",
  "eventCallDesc": "complain",           // From selected category
  "streetCode": "898",
  "streetDesc": "קרל פופר",
  "houseNumber": "11",                   // From selected street number
  "callerFirstName": "aaaaa",            // User's first name
  "callerLastName": "bbbb",              // User's last name
  "callerTZ": "111111111",               // User's ID
  "callerPhone1": 222222222,             // User's phone
  "callerEmail": "aaaa@gmail.com",       // User's email
  "contactUsType": "3"
}
```

#### Data Mapping
- **From User Data**:
  - `callerFirstName`: User's first name
  - `callerLastName`: User's last name
  - `callerTZ`: User's ID number
  - `callerPhone1`: User's phone number
  - `callerEmail`: User's email address

- **From Category Selection**:
  - `eventCallDesc`: Category's event_call_desc field

- **From Street Number Selection**:
  - `houseNumber`: Street number's house_number field

- **Fixed Values**:
  - `eventCallSourceId`: 4
  - `cityCode`: "7400"
  - `cityDesc`: "נתניה"
  - `eventCallCenterId`: "3"
  - `streetCode`: "898"
  - `streetDesc`: "קרל פופר"
  - `contactUsType`: "3"

#### Response Handling
- **Success (200)**: Show success popup, restart to categories page
- **Error (4xx/5xx)**: Show error popup, restart to categories page
- **Network Error**: Show error popup, restart to categories page

## Internationalization (i18n)

### Language Support
- **Hebrew**: RTL layout, Hebrew text
- **English**: LTR layout, English text
- **French**: LTR layout, French text
- **Russian**: LTR layout, Russian text

### Translation Keys
- All UI text elements
- Error messages
- Success messages
- Form labels and placeholders
- Popup content

### RTL Support
- CSS direction property for Hebrew
- Text alignment adjustments
- Icon positioning for RTL layout

## Security Considerations

### Data Validation
- Client-side validation for all form inputs
- Server-side validation (if applicable)
- Input sanitization to prevent XSS
- Email format validation

### Local Storage Security
- Sensitive data stored locally only
- No transmission of personal data to external services (except final submission)
- Clear data option for users

### API Security
- HTTPS-only communication
- Proper headers to mimic legitimate browser requests
- Rate limiting consideration
- Error handling without exposing sensitive information

## Performance Optimization

### Data Loading
- Lazy loading for images
- Caching of Supabase data in session state
- Efficient grid rendering for large datasets

### Search Performance
- Debounced search input
- Local filtering without server requests
- Optimized search algorithms

### API Performance
- Connection pooling for HTTP requests
- Timeout handling
- Retry logic for failed requests

## Error Handling

### User Experience
- Graceful degradation for network issues
- Clear error messages in user's language
- Recovery options for all error states

### Technical Errors
- Logging of errors for debugging
- Fallback content for failed data loads
- Retry mechanisms for API calls
- Network timeout handling

### API Error Scenarios
- Network connectivity issues
- Server errors (5xx)
- Client errors (4xx)
- Invalid data format
- Rate limiting responses

## Testing Strategy

### Unit Tests
- Form validation functions
- Data transformation utilities
- Language switching logic
- API payload preparation

### Integration Tests
- Supabase data loading
- HTTP API integration
- Local storage operations
- Multipart form data creation

### User Acceptance Tests
- Complete user flows (new and existing users)
- Mobile responsiveness
- Multilingual functionality
- API submission scenarios

## Application Modes: Release and Debug

The application supports two modes of operation:

### 1. Release Mode
- **Purpose**: Production use.
- **Behavior**: All features are live. The app sends real HTTP POST requests to the Netanya Municipality API endpoint.
- **Configuration**: Set the environment variable `APP_MODE=release` (or `DEBUG=False`).

### 2. Debug Mode
- **Purpose**: Development and testing.
- **Behavior**: The app does NOT send real HTTP POST requests. Instead, it uses a mock server or function to simulate API responses. This prevents accidental submissions to the real municipality system during development.
- **Configuration**: Set the environment variable `APP_MODE=debug` (or `DEBUG=True`).
- **Mocking**: The mock server should return a simulated JSON response with a fake ticket number, mimicking the real API's structure.

#### Example Mock Response
```json
{
  "ResultCode": 200,
  "ErrorDescription": "Mocked success.",
  "ResultStatus": "SUCCESS CREATE",
  "ResultData": {
    "incidentGuid": "mock-guid-1234",
    "incidentNumber": "MOCK-0001"
  },
  "data": "MOCK-0001"
}
```

### Mode Selection
- The application checks the environment variable at startup to determine which mode to use.
- All API service logic should branch based on this mode.

## Deployment and Configuration (updated)

### Environment Variables
- `APP_MODE`: Set to `release` for production or `debug` for development/testing.
- `DEBUG`: Alternative boolean flag (True/False) for backward compatibility.
- `SUPABASE_URL` and `SUPABASE_KEY`: As before.
- `Netanya Municipality API endpoint`: As before.

### API Service Logic
- In debug mode, use a mock function or local server to simulate API responses.
- In release mode, send real requests to the municipality endpoint.

### Testing
- All integration and end-to-end tests should run in debug mode by default, using the mock server.
- Add tests to verify both real and mock API logic.

## Future Enhancements

### Potential Additions
- User analytics and tracking
- Advanced search filters
- Data export functionality
- Admin panel for content management
- Push notifications
- Offline mode support
- API response caching
- Request/response logging

### Scalability
- Database indexing for performance
- CDN integration for images
- Caching strategies for frequently accessed data
- Load balancing for API requests 

## Additional Implementation Notes (2024-06)

- **Email Field**: The email field is optional. Validation and UI should not require it.
- **Ticket History**: Ticket numbers from successful submissions should be saved locally in an array for possible future features (e.g., ticket history display).
- **Translations**: All translations should be loaded from external files (e.g., JSON or YAML) so they can be easily modified manually.
- **Mobile Optimization**: The UI must be fully mobile-optimized, including touch-friendly controls and large buttons.
- **Multipart/Form-Data & File Upload**: The POST request must use multipart/form-data. The code should be structured to allow easy addition of file upload support in the future, but file upload is not implemented yet.
- **No Logout/Clear Data**: There is no need for a 'logout' or 'clear my data' button.
- **Hardcoded Street Codes**: `streetCode` and `streetDesc` are always the same, hardcoded in the API request.
- **Mock API**: In debug mode, the mock API always returns a success response for UI and flow debugging.
- **Initial Data**: Initial data for categories and street numbers will be added to the database later. Use mock data for development and testing.
- **Future Features**: Structure the code to allow easy addition of file upload and ticket history features. 