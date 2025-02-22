DROP TABLE IF EXISTS SFS_CREDENTIAL;
DROP TABLE IF EXISTS SFS_THRESHOLD;
DROP TABLE IF EXISTS SFS_COMPANY;
DROP TABLE IF EXISTS SFS_PRODUCT;
DROP TABLE IF EXISTS SFS_OPERATION;
DROP TABLE IF EXISTS SFS_COMPOSITION;
DROP TABLE IF EXISTS SFS_CERTIFICATION_BODY;
DROP TABLE IF EXISTS SFS_COMPENSATION_ACTION;


CREATE TABLE SFS_CREDENTIAL (
    id_credential INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    topt_secret TEXT NOT NULL,
    public_key TEXT,
    private_key TEXT,
    role_credential TEXT,
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE SFS_THRESHOLD (
    operation_threshold TEXT NOT NULL,
    product_threshold TEXT NOT NULL,
    threshold_maximum REAL NOT NULL,
    tipo TEXT NOT NULL,
    PRIMARY KEY (operation_threshold, product_threshold)
);

CREATE TABLE SFS_COMPANY (
    id_company INTEGER PRIMARY KEY AUTOINCREMENT,
    id_credential INTEGER NOT NULL,
    name_company TEXT NOT NULL,
    type_company CHECK(type_company IN ('Farmer', 'Producer', 'Logistics', 'Retailer', 'CertificationBody')),
    location_company TEXT NOT NULL,
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_credential) REFERENCES SFS_CREDENTIAL(id_credential)
);


CREATE TABLE SFS_PRODUCT (
    id_product INTEGER PRIMARY KEY AUTOINCREMENT,
    name_product TEXT NOT NULL,
    type_product TEXT,
    quantity_product INTEGER NOT NULL,
    status_product INTEGER,
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE SFS_OPERATION (
    id_operation INTEGER PRIMARY KEY AUTOINCREMENT,
    id_company INTEGER NOT NULL,
    id_product INTEGER NOT NULL,
    co2_footprint REAL NOT NULL,
    operation_description TEXT,
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_company) REFERENCES SFS_COMPANY(id_company),
    FOREIGN KEY (id_product) REFERENCES SFS_PRODUCT(id_product)
);


CREATE TABLE SFS_COMPOSITION (
    cod_product INTEGER NOT NULL,
    cod_raw_material INTEGER NOT NULL,
    PRIMARY KEY (cod_product, cod_raw_material)
);


CREATE TABLE SFS_CERTIFICATION_BODY (
    id_certification_body INTEGER PRIMARY KEY AUTOINCREMENT,
    id_product INTEGER NOT NULL,
    id_company INTEGER NOT NULL,
    description TEXT,
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_company) REFERENCES SFS_COMPANY(id_company),
    FOREIGN KEY (id_product) REFERENCES SFS_PRODUCT(id_product)
);



CREATE TABLE SFS_COMPENSATION_ACTION (
    id_compensation_action INTEGER PRIMARY KEY AUTOINCREMENT,
    id_company INTEGER NOT NULL,
    name_compensation_action TEXT NOT NULL,
    co2_compensation REAL NOT NULL,
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_company) REFERENCES SFS_COMPANY(id_company)
);