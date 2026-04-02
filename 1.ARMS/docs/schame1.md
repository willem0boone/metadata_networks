```mermaid
flowchart TB

%% -------------------------
%% ETN
%% -------------------------
B[External Service: ETN]

%% -------------------------
%% 1.extract_ETN_ARMS.py
%% -------------------------
subgraph Python Wrapper
    C["/R/config/config_ETN_ARMS_search.yaml"]
    A["/R/extract_ETN_ARMS.R"]
end

B --> A
C --> A

A --> E["../etn_arms_export/deployment_ARMS.csv"]

%% -------------------------
%% Static config
%% -------------------------
F["config/config.json"]

%% -------------------------
%% Passport pipeline
%% -------------------------
G[2.form_passport.py]

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
H --> M[verify if exist]
M <--> L

%% -------------------------
%% Submission (separate, no coupling)
%% -------------------------
L --> O2