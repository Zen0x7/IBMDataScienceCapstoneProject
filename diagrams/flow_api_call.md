flowchart TD
    A[Start] --> B{Import necessary libraries};
    B --> C{Define function };
    C --> D[Try to make a GET request to the URL];
    D -- Successful (status code 200) --> E[Convert response to JSON];
    E --> F[Return JSON data];
    D -- Unsuccessful --> G[Print error message status code and reason];
    G --> H[End Error];
    F --> I[End Success];

    C -- Exception --> J[Print error message];
    J --> H;
    
    subgraph "Necessary Libraries"
        B1[requests]
        B2[pandas]
    end

    style B fill:#ccf,stroke:#888,stroke-width:2px