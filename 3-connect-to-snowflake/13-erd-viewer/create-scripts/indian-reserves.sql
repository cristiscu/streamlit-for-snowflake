CREATE OR REPLACE DATABASE "IndianReserves";

CREATE TABLE "Reserves" (
 "reserve_id" INT NOT NULL PRIMARY KEY,
 "reserve_number" VARCHAR(6) NOT NULL,
 "reserve_name" VARCHAR(100) NOT NULL,
 "contact_name" VARCHAR(100)
);
 
CREATE TABLE "Bands" (
 "band_id" INT NOT NULL PRIMARY KEY,
 "band_number" VARCHAR(4) NOT NULL,
 "band_name" VARCHAR(100) NOT NULL,
 "tribal_council" VARCHAR(100)
);
CREATE TABLE "ReservesToBands" (
 "reserve_id" INT NOT NULL
   FOREIGN KEY REFERENCES "Reserves" ("reserve_id"),
 "band_id" INT NOT NULL
    FOREIGN KEY REFERENCES "Bands" ("band_id"),
 PRIMARY KEY ("reserve_id", "band_id")
);
CREATE TABLE "Provinces" (
 "province_code" VARCHAR(2) NOT NULL PRIMARY KEY,
 "province_name" VARCHAR(50) NOT NULL
);
CREATE TABLE "ReservesToProvinces" (
 "reserve_id" INT NOT NULL
   FOREIGN KEY REFERENCES "Reserves" ("reserve_id"),
 "province_code" VARCHAR(2) NOT NULL
   FOREIGN KEY REFERENCES "Provinces" ("province_code"),
 PRIMARY KEY ("reserve_id", "province_code")
);
CREATE TABLE "BandsToProvinces" (
 "band_id" INT NOT NULL
   FOREIGN KEY REFERENCES "Bands" ("band_id"),
 "province_code" VARCHAR(2) NOT NULL
   FOREIGN KEY REFERENCES "Provinces" ("province_code"),
 PRIMARY KEY ("band_id", "province_code")
);
CREATE TABLE "Offices" (
 "office_id" INT NOT NULL PRIMARY KEY,
 "office_name" VARCHAR(200),
 "address" VARCHAR(200)
);
CREATE TABLE "ReservesToOffices" (
 "reserve_id" INT NOT NULL
   FOREIGN KEY REFERENCES "Reserves" ("reserve_id"),
 "office_id" INT NOT NULL
   FOREIGN KEY REFERENCES "Offices" ("office_id"),
 PRIMARY KEY ("reserve_id", "office_id")
);
CREATE TABLE "BandsToOffices" (
 "band_id" INT NOT NULL
   FOREIGN KEY REFERENCES "Bands" ("band_id"),
 "office_id" INT NOT NULL
   FOREIGN KEY REFERENCES "Offices" ("office_id"),
 PRIMARY KEY ("band_id", "office_id")
);
CREATE TABLE "Users" (
 "user_id" INT NOT NULL PRIMARY KEY,
 "user_name" VARCHAR(255) NOT NULL,
 "last_logon" TIMESTAMP NOT NULL
);
CREATE TABLE "WorksWith" (
 "user_id" INT NOT NULL
   FOREIGN KEY REFERENCES "Users" ("user_id"),
 "works_with_id" INT NOT NULL
   FOREIGN KEY REFERENCES "Users" ("user_id"),
 "assignment" VARCHAR(255),
 PRIMARY KEY ("user_id", "works_with_id")
);
CREATE TABLE "UsersToReserves" (
 "user_id" INT NOT NULL
   FOREIGN KEY REFERENCES "Users" ("user_id"),
 "reserve_id" INT NOT NULL
   FOREIGN KEY REFERENCES "Reserves" ("reserve_id"),
 PRIMARY KEY ("user_id", "reserve_id")
);
CREATE TABLE "UsersToBands" (
 "user_id" INT NOT NULL
   FOREIGN KEY REFERENCES "Users" ("user_id"),
 "band_id" INT NOT NULL
   FOREIGN KEY REFERENCES "Bands" ("band_id"),
 PRIMARY KEY ("user_id", "band_id")
);
CREATE TABLE "Roles" (
 "role_id" INT NOT NULL PRIMARY KEY,
 "role_name" VARCHAR(100) NOT NULL,
 "description" VARCHAR(1000)
);
CREATE TABLE "UsersToRoles" (
 "user_id" INT NOT NULL
   FOREIGN KEY REFERENCES "Users" ("user_id"),
 "role_id" INT NOT NULL
   FOREIGN KEY REFERENCES "Roles" ("role_id"),
 PRIMARY KEY ("user_id", "role_id")
);
CREATE TABLE "Privileges" (
 "privilege_id" INT NOT NULL PRIMARY KEY,
 "privilege_code" VARCHAR(4) NOT NULL,
 "description" VARCHAR(1000)
);
CREATE TABLE "PrivilegesToRoles" (
 "privilege_id" INT NOT NULL
   FOREIGN KEY REFERENCES "Privileges" ("privilege_id"),
 "role_id" INT NOT NULL
   FOREIGN KEY REFERENCES "Roles" ("role_id"),
 PRIMARY KEY ("privilege_id", "role_id")
);