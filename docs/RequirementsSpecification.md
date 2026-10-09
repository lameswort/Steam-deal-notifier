# Steam Deal Notifier - requirements Specification
## 1. Functional requirements
Functional requirements describe the tasks that the application will perform.
## FR-01: steam Wishlist Integration
The application will prompt users to sign into their steam profiles, after which it will acquire their steam Wishlist Data.
## FR-02: Sale Detection
The application will check a users Wishlist for active discounts. 
## FR-03: Price History Tracking
The application will retrieve historical game prices for the game that is on sale.
## FR-04: Deal Quality Analysis
The system will analyze the current sale in comparison with the sale history.
## FR-05: Sale Notifications
The application will notify users of the sale through desktop notifications, and inform them how good the deal is.
## 2. Non-Functional Requirements
## NFR-01: Usability 
The application will have a simple user interface.
## NFR-02: Reliability
The system will handle errors without causing the app to crash or infinitely loop.
## NFR-03: Security
API credentials will be securely stored.
## NFR-04: Accessibility
Information will be efficiently communicated and and the user interface will be easy to navigate.
## 3. Assumptions and Constraints 
- Application will require and internet connection.
- Wishlist access may depend on account privacy settings.
- API rate limits.
- Application will be developed for only windows.
