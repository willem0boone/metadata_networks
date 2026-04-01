```mermaid
flowchart TB

%% -------------------------
%% ETN
%% -------------------------
B[External Service: ETN]

%% -------------------------
%% Python wrapper
%% -------------------------
subgraph Python Wrapper
    C["config.yaml (ETN filter args)"]
    A[R Script: extract_ETN_ARMS.R]
end

B --> A
C --> A

A --> E["deployments.csv (variable args)"]

%% -------------------------
%% Static config
%% -------------------------
F["config.json (static args)"]

%% -------------------------
%% Passport pipeline
%% -------------------------
G[Python: create_passport.py]

E --> G
F --> G

H{Passport already exists?}

G --> H

%% -------------------------
%% Passport logic (no API coupling)
%% -------------------------
H -- No --> J["Generate WIGOS ID (OceanOps)"]
J --> K[Create new passport.json]

H -- Yes --> I[Update existing passport.json]

%% -------------------------
%% OceanOps client
%% -------------------------
subgraph OceanOpsClient
    O1[post_wigos_id]
    O2[post_passport]
end

%% Correct direction: API drives generation
O1 --> J

%% -------------------------
%% Storage (local state)
%% -------------------------
L[(Passports Directory)]

K --> L
I --> L

%% -------------------------
%% Submission (separate, no coupling)
%% -------------------------
L --> O2