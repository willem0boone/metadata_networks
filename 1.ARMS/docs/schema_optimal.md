```mermaid
flowchart TB

%% -------------------------
%% Section 1: ETN
%% -------------------------

A((Operators)) --> id1[(ETN database)]

    

id1--> B[/"Extract_ETN_ARMS.py"/]
B --> C["deployments.json (variable args)"]

%% -------------------------
%% Section 2: create passports
%% -------------------------
F["config.json (static args)"]


G[Python: create_passport.py]

C --> G
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

