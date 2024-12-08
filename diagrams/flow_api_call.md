flowchart TD
    B{Start} --> C{Function get_json_from};
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
    end