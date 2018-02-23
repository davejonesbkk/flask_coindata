drop table if exists prices;
create table prices (
  id integer primary key autoincrement,
  coin text not null,
  usd int not null
);