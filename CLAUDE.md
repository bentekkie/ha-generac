# Generac Home Assistant Plugin Development Notes

## Current Authentication Challenge

The Generac Home Assistant plugin currently uses automated login with username/password, but this fails due to recaptcha protection on the web login flow.

## Cookie-Based Authentication Implementation (COMPLETED)

### Problem
- Web login requires recaptcha which prevents automated authentication
- Users can manually login via browser but plugin can't automate this

### Solution Implemented
Added cookie-based authentication as alternative to username/password:

### Files Modified
1. **`const.py`** - Added `CONF_COOKIES` constant
2. **`api.py`** - Modified `GeneracApiClient` to accept cookies parameter
3. **`config_flow.py`** - Updated config form to accept cookies input
4. **`__init__.py`** - Pass cookies to API client
5. **`translations/en.json`** - Added cookie instructions for users

### How It Works
- Users can provide either username/password OR browser cookies
- Plugin validates cookies by making test API call to `/v2/Apparatus/list`
- Falls back to traditional login if cookies fail and credentials provided
- Instructions help users extract cookies from browser DevTools

### Cookie Format Expected
```
name1=value1; name2=value2; name3=value3
```

## Mobile App Authentication Implementation (COMPLETED)

### Mobile App Analysis Results
Successfully analyzed Generac iOS mobile app traffic using Charles Proxy:

**Key Findings:**
- **API Version**: Mobile app uses `/api/v5/Apparatus/list` (vs web v2)
- **Authentication**: JWT Bearer tokens from Azure B2C
- **User-Agent**: `mobilelink/75633 CFNetwork/3826.600.41 Darwin/24.6.0`
- **Base URL**: Same `https://app.mobilelinkgen.com/api`

**JWT Token Details:**
- **Issuer**: `https://generacconnectivity.b2clogin.com/6cb336d5-d73b-4714-8deb-33d49a8cc484/v2.0/`
- **Audience**: `cf3e2bfb-2d0c-47dd-8067-bf59a6f88ed7`
- **Algorithm**: RS256
- **Contains**: Email, subscription ID, expiration

### Mobile Token Authentication Implementation
Added JWT token-based authentication as third auth method:

**Files Modified:**
1. **`const.py`** - Added token auth constants and method definitions
2. **`api.py`** - Enhanced `GeneracApiClient` to support JWT tokens with mobile headers
3. **`config_flow.py`** - Added multi-step config flow with auth method selection
4. **`__init__.py`** - Updated client initialization to support all auth methods

### v5 API Integration (COMPLETED)
Enhanced plugin to use mobile app's v5 API endpoints with expanded sensor support:

**API Improvements:**
- **Apparatus List**: `/api/v5/Apparatus/list` with v2 fallback
- **Apparatus Details**: `/api/v1/Apparatus/details/{id}` (more reliable than v5)
- **Property Type Mapping**: Updated for v5 API property types
- **Enhanced Data Models**: Added v5-specific fields and structures

**New Sensors Added:**
- **Exercise Minutes** (type 95) - Generator exercise duration
- **Fuel Type** (type 88) - Natural Gas/Propane detection
- **Network Type** - WiFi/Ethernet connection method
- **Current Alarm** - Active alarm codes
- **Service Mode** - Service mode status (binary)
- **VPP Enrolled** - Virtual Power Plant enrollment (binary)
- **Active VPP Event** - VPP event status (binary)
- **Disconnected Notifications** - Notification settings (binary)

**Property Type Mapping Changes:**
- Battery Voltage: v5 type 70 (was v2 type 69)
- Engine Hours: v5 type 71 (was v2 type 70)  
- Hours of Protection: v5 type 32 (was v2 type 31)
- Exercise Minutes: v5 type 95 (new)
- Fuel Type: v5 type 88 (new)

**Three Authentication Methods Now Supported:**
1. **Username/Password** - Original web login flow with CSRF/B2C
2. **Browser Cookies** - Manual cookie extraction from web session  
3. **JWT Token** - Mobile app token for direct API access

### Mobile App Traffic Capture Process
For users wanting to extract their own JWT tokens:

1. **Setup Charles Proxy:**
   - Install Charles root certificate on iOS device
   - Enable SSL Proxying for `*.mobilelinkgen.com` 
   - Trust certificate in iOS Settings

2. **Capture Authentication:**
   - Clear Generac app data/logout
   - Start Charles recording
   - Login to Generac mobile app
   - Find Authorization header: `Bearer eyJhbGciOiJSUzI1NiIs...`

## Implementation Status
- ✅ Cookie-based authentication framework
- ✅ JWT token-based authentication 
- ✅ Multi-method config flow
- ✅ API client with v5 endpoint support
- ✅ Mobile app traffic analysis
- ✅ All authentication methods working
- ✅ v5 API integration with enhanced sensors
- ✅ Backward compatibility with v2/v1 APIs
- ✅ Property type mapping updates
- ✅ New binary sensors for v5 features

## Usage Instructions for Cookie Method
1. Login to Generac web app in browser
2. Open DevTools (F12) → Application/Storage → Cookies
3. Copy all cookies for `mobilelinkgen.com` domain
4. Paste into Home Assistant config as: `name1=value1; name2=value2`

## Technical Notes
- Current code uses `X-Csrf-Token` but browser sends `X-XSRF-TOKEN`
- May need to update header name for full compatibility
- Mobile app analysis will likely reveal better approach than browser cookies