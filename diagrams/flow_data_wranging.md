flowchart TD
    B{Start} --> C{Invoke get_json_from with param URL and store in DATA};
    C --> D[Use pandas json_normalize function to create DataFrame]

    subgraph "Necessary Libraries"
        B1[pandas]
    end