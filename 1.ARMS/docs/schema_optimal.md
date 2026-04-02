```mermaid
flowchart TB

%% -------------------------
%% Section 1: ETN
%% -------------------------

B[External Service: ETN]

subgraph Python Wrapper
    C["config.yaml (ETN filter args)"]
    A[R Script: extract_ETN_ARMS.R]
end

B --> A
C --> A

A --> E["deployments.csv (variable args)"]

%% -------------------------
%% Section 2: create passports
%% -------------------------
F["config.json (static args)"]


G[Python: create_passport.py]

E --> G
F --> G

H{Passport already exists?}

G --> H


H -- No -->  K[Create new passport.json]

H -- Yes --> I[Update existing passport.json]

%% -------------------------
%% Section 3: oceanopsclient
%% -------------------------
subgraph OceanOpsClient
    O1[post_wigos_id]
    O2[post_passport]
    O3[search_pltf]
end

L[(Passports Directory)]

K --> L
I --> L
H <--> M[verify if exist]
M <--> O3

%% -------------------------
%% Section 4: wigos
%% -------------------------

N["passport.json"]

O{"has wigos? "}

L --> N
N --> O
O -- No --> O1 --> N
O -- Yes --> O2



%% -------------------------
%% Submission (separate, no coupling)
%% -------------------------
