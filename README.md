Install PostgreSQL
========================================================================
1. Download PostgreSQL
https://www.enterprisedb.com/downloads/postgres-postgresql-downloads

2. Set up PostgreSQL

4. Buka SQL Shell (psql), untuk membuat koneksi ke database
Tekan ENTER 
Server [localhost]: *Tekan ENTER*
Database [postgres]: *Tekan ENTER* 
Port [5432]:*Tekan ENTER*
Username [postgres]: *Tekan ENTER*
Password for user postgres: admin

notes: untuk password disesuaikan saja
========================================================================
Install Dbeaver dan Buat Koneksi
1. install dbeaver dari link berikut:
https://dbeaver.io/files/dbeaver-ce-latest-x86_64-setup.exe

2. set up dbeaver

4. Buat koneksi baru
- pilih PostgreSQL
- isi form (sesuai pada saat isntall postgresql)
Host = localhost
Port = 5432
username = postgres
password = admin
- Test Connection 
- Finish
========================================================================
Buat Schema

CREATE SCHEMA public AUTHORIZATION postgres;

Buat Table dan isi tabel dengan data

1. m_chiller
CREATE TABLE public.m_chiller (
	chiller_id varchar NOT NULL,
	subdist_id varchar NULL,
	CONSTRAINT m_chiller_pk PRIMARY KEY (chiller_id)
);

INSERT INTO public.m_chiller
(chiller_id, subdist_id)
VALUES
('chiller_01', 'sd01')
('chiller_02', 'sd02')
('chiller_03', 'sd03');

2. m_subdist
CREATE TABLE public.m_subdist (
	subdist_id varchar NOT NULL,
	subdist_name varchar NOT NULL,
	"location" varchar NULL,
	owner_id varchar NOT NULL,
	pic varchar NULL,
	CONSTRAINT m_subdist_pk PRIMARY KEY (subdist_id, owner_id)
);

INSERT INTO public.m_subdist
(subdist_id, subdist_name, "location", owner_id, pic)
VALUES
('sd01', 'subdist01', 'tangerang', 'own01', 's01')
('sd02', 'subdist02', 'jakarta', 'own01', 's01')
('sd03', 'subdist03', 'tangerang', 'own02', 's02')
('sd04', 'subdist04', 'depok', 'own3', 's03')
('sd05', 'subdist05', 'bekasi', 'own04', 's03');

3. m_user
CREATE TABLE public.m_user (
	username varchar NOT NULL,
	"name" varchar NULL,
	"password" varchar NOT NULL,
	user_type varchar NULL,
	CONSTRAINT m_user_pk PRIMARY KEY (username)
);

INSERT INTO public.m_user
(username, "name", "password", user_type)
VALUES
('s01', 'Imron Kurniawan', '$2y$10$0IVB4Qw7ZyQe.ldbEyLLS.GzB1kurEd7oBmHIfdv6ko6XhQ0UOuQq', 'sales')
('s02', 'Debby Sanjaya', '$2y$10$0IVB4Qw7ZyQe.ldbEyLLS.GzB1kurEd7oBmHIfdv6ko6XhQ0UOuQq', 'sales')
('d01', 'Cindya Naomi', '$2y$10$0IVB4Qw7ZyQe.ldbEyLLS.GzB1kurEd7oBmHIfdv6ko6XhQ0UOuQq', 'admin');

4. t_chiller_detection
CREATE TABLE public.t_chiller_detection (
	docno varchar DEFAULT uuid_generate_v4() NOT NULL,
	subdist_id varchar NULL,
	chiller_id varchar NULL,
	path_image varchar NULL,
	send_date timestamp NULL,
	detections varchar NULL,
	CONSTRAINT t_chiller_detection_unique UNIQUE (docno)
);
