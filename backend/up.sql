BEGIN;
CREATE TABLE "hr_address" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "address_line1" varchar(100) NOT NULL, "address_line2" varchar(100) NULL, "city" varchar(100) NOT NULL, "zip_code" integer NOT NULL);
CREATE TABLE "hr_basicinfo" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NOT NULL, "email" varchar(254) NOT NULL);
CREATE TABLE "hr_contract" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "hiring_date" date NOT NULL, "job_title" varchar(100) NOT NULL);
CREATE TABLE "hr_team" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NOT NULL);
CREATE TABLE "hr_employee" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "is_manager" bool NOT NULL, "address_id" bigint NOT NULL UNIQUE REFERENCES "hr_address" ("id") DEFERRABLE INITIALLY DEFERRED, "basic_info_id" bigint NOT NULL UNIQUE REFERENCES "hr_basicinfo" ("id") DEFERRABLE INITIALLY DEFERRED, "contract_id" bigint NOT NULL UNIQUE REFERENCES "hr_contract" ("id") DEFERRABLE INITIALLY DEFERRED, "manager_id" bigint NULL REFERENCES "hr_employee" ("id") DEFERRABLE INITIALLY DEFERRED, "team_id" bigint NULL REFERENCES "hr_team" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE INDEX "hr_employee_manager_id_e98ea225" ON "hr_employee" ("manager_id");
CREATE INDEX "hr_employee_team_id_ff63a1e5" ON "hr_employee" ("team_id");
COMMIT;
