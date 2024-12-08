flowchart TD
    B{Start} --> C{Import Request Library};
    C --> D[Connect and Fetch SpaceX Endpoint using HTTP Client];
    D --> E[Parse and Load to the DataFrame]

    subgraph "Necessary Libraries"
        B1[requests]
        B2[pandas]
    end