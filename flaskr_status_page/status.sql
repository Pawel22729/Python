drop table if exists apps;

create table apps (
    id integer primary key autoincrement,
    application text not null,
    version text not null,
    host text not null
);
