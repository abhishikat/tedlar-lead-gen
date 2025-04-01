# DuPont Tedlar Lead Generation AI Agent

This repository contains a prototype AI agent for automating lead generation and outreach for DuPont Tedlar's Graphics & Signage team. The agent can identify potential leads, qualify them against an Ideal Customer Profile (ICP), find key decision-makers, and generate personalized outreach messages.

## Features

- **Data Collection**: Automatically gather information about relevant industry events, associations, and companies.
- **Lead Qualification**: Score and prioritize companies based on alignment with DuPont Tedlar's ICP.
- **Stakeholder Identification**: Locate key decision-makers at qualified companies.
- **Personalized Outreach**: Generate tailored outreach messages for each stakeholder.
- **Dashboard Visualization**: Present findings in a clear, actionable format.

## Installation

1. Clone this repository:
```bash
git clone https://github.com/abhishikat/tedlar-lead-gen.git
cd tedlar-lead-gen
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

The system is configured through the `config.yaml` file. Key settings include:

- **Target Events & Associations**: Industry events and associations relevant to DuPont Tedlar.
- **ICP Criteria**: Ideal Customer Profile criteria for qualifying leads.
- **API Keys**: Integration points for external services (LinkedIn Sales Navigator, Clay API, etc.).

## Usage

### Running the Full Pipeline

To run the complete lead generation pipeline:

```bash
python main.py
```

This will:
1. Collect data about events, associations, and companies
2. Qualify leads based on ICP criteria
3. Identify stakeholders at qualified companies
4. Generate personalized outreach messages
5. Save all data for dashboard visualization

### Running Individual Modules

You can also run individual modules separately:

```bash
# Data Collection
python -m src.data_collection

# Lead Qualification
python -m src.lead_qualification data/companies.json

# Stakeholder Identification
python -m src.stakeholder_finder data/qualified_leads.json

# Personalization
python -m src.personalization data/stakeholders.json
```

### Using the Dashboard

To view the results in a dashboard:

```bash
python -m dashboard.app
```

The dashboard provides:
- Overview of qualified leads
- Detailed company information
- Stakeholder profiles
- Personalized outreach messages
- Filtering and sorting capabilities

## Extending the Prototype

### Adding Real API Integrations

To integrate with real data sources:

1. Add API credentials to the configuration file
2. Update the relevant module with proper API client implementation
3. Replace mock data generation with actual API calls

Key integration points:
- LinkedIn Sales Navigator API for stakeholder data
- Clay API for contact enrichment
- Event APIs for real event data

### Enhancing Lead Qualification

To improve lead qualification:
- Add more sophisticated scoring algorithms
- Incorporate machine learning for predictive qualification
- Integrate with CRM systems for historical data

### Improving Personalization

To enhance outreach personalization:
- Integrate with a production OpenAI API implementation
- Add feedback loops to improve message effectiveness
- Incorporate company-specific knowledge bases

## Project Structure

```
tedlar-lead-gen/
├── README.md                   # Project documentation
├── requirements.txt            # Dependencies
├── config.yaml                 # Configuration settings
├── main.py                     # Entry point
├── src/
│   ├── __init__.py
│   ├── data_collection.py      # Event and association scraping
│   ├── lead_qualification.py   # Company filtering and prioritization
│   ├── stakeholder_finder.py   # Decision-maker identification
│   ├── personalization.py      # Outreach message generation
│   └── utils.py                # Helper functions
├── data/
│   ├── events.json             # Collected event data
│   ├── companies.json          # Qualified companies
│   └── stakeholders.json       # Decision-makers data
└── dashboard/
    ├── __init__.py
    ├── app.py                  # Streamlit dashboard
    └── components.py           # UI components
```

## Notes on Implementation

This prototype uses synthetic data for demonstration purposes. In a production environment, it would integrate with:

1. **Real Data Sources**: LinkedIn Sales Navigator, ZoomInfo, event websites, etc.
2. **LLM Services**: OpenAI API for advanced personalization
3. **Authentication**: Proper API key management and security
4. **Error Handling**: Robust error handling and retry logic
5. **Monitoring**: Usage tracking and performance monitoring

## Future Enhancements

Potential improvements for a production version:

1. **Integration with CRM**: Salesforce, HubSpot, etc.
2. **Email Automation**: Direct sending of outreach messages
3. **Feedback Loop**: Track response rates and optimize messaging
4. **Advanced Analytics**: Conversion tracking and ROI measurement
5. **Multi-Industry Support**: Configurable for different DuPont product lines



## Contact

[Abhishikat Soni]