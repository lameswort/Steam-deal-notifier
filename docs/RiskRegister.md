# Risk Register

## Purpose

This document identifies potential risks that could affect the development of our Steam Deal Notifier application and how we plan to manage them.

## Risk Assessment Scale

### Probability
- Low (L): Unlikely to occur
- Medium (M): May occur during the project
- High (H): Likely to occur during the project

### Impact
- Low (L): Minor effect on project progress
- Medium (M): Noticeable impact on schedule, quality, or scope
- High (H): Significant impact on project success

### Risk Status Definitions

- Open: Risk currently exists and requires monitoring.
- Mitigated: Actions have reduced the likelihood or impact.
- Closed: Risk is no longer relevant.
- Occurred: Risk occurred and required response actions.


## Risk Register

| Risk ID | Category | Risk Description | Probability | Impact | Mitigation Strategy | Owner | Status |
|----------|------------|-----------------|-------------|---------|---------------------|--------|---------|
| R-01 | Technical | The Steam API may not provide all the information needed for the application. | M | H | Research the Steam API early and look for alternative ways to retrieve the required data. | Team | Open |
| R-02 | Technical | Historical price data may be unavailable or incomplete for certain games.  | H | H | Research available price history sources and inform users when there is not enough data. | Team | Open |
| R-03 | Technical | The application may have issues retrieving or updating game prices. | M | H | Test price retrieval regularly and add error handling for failed requests. | Team | Open |
| R-04 | Schedule | The project may take longer than expected to complete. | M | H | Divide the project into smaller tasks and prioritize the most important features. | Team | Open |
| R-05 | Knowledge | Team members may have limited experience with certain technologies used in the project. | M | M | Research unfamiliar technologies and begin testing them early in development. | Team | Open |
## Risk Management

The team will review the risk register throughout development and update it when new risks are identified or existing risks change.
