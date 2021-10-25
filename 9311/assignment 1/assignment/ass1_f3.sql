-- Assignment 1 Stage 2
-- Schema for the et.org events/ticketing site
--
-- Written by Huiyao Zuo (z5196480)
--
-- Conventions:
-- - all entity table names are plural
-- - most entities have an artifical primary key called "id"
-- - foreign keys are named after the relationship they represent

-- Generally useful domains

create domain URLValue as
	varchar(100) check (value like 'http://%');

create domain EmailValue as
	varchar(100) check (value like '%@%.%');

create domain GenderValue as
	char(1) check (value in ('m','f','n'));

create domain ColourValue as
	char(7) check (value ~ '#[0-9A-Fa-f]{6}');

create domain LocationValue as varchar(40)
	check (value ~ E'^-?\\d+\.\\d+,-?\\d+\.\\d+$');

	-- latitiude and longitude in format used by Google Maps
	-- e.g. '-33.916369,151.23024' (UNSW)

create domain NameValue as varchar(50);

create domain LongNameValue as varchar(100);


-- PLACES: addresses, geographic locations, etc.

create table places (
	id          serial,      -- integer default nextval('some_seq_or_other')
	primary key (id) ,
    name        LongNameValue ,
    address     text ,
    city        LongNameValue,
    state       LongNameValue ,
    country     LongNameValue ,
    postalCode  integer ,
    gpsCoords   LocationValue
);


-- PAGEs: settings for pages in et.org

create table pageColours (
	id       serial,
	primary key (id) ,
	ownedBy            serial,
	maintext     text ,
	heading      LongNameValue,
	headtext     text ,
	borders      ColourValue ,
	boxes        ColourValue ,
	links        URLValue ,
	background   ColourValue ,
	isTemplate   boolean ,
	name         LongNameValue
);
alter table pageColours
    add foreign key (ownedBy) references users(id) ;   --ownedby relationship


-- PEOPLE: information about various kinds of people
-- Users are People who can login to the system
-- Contacts are people about whom we have minimal info
-- Organisers are "entities" who organise Events

create table people (
	id     serial ,
	primary key (id) ,
	givenName    NameValue not null ,
	email        EmailValue not null ,
	familyName   NameValue
);

create table users (
	id       serial ,
	primary key (id) ,
	gender       GenderValue ,
	birthday     date ,
	phone        integer ,
	blog         URLValue ,
	showName     LongNameValue ,
	password     varchar(30) not null ,
	website      URLValue ,
	billingAddress       text not null ,
	homeAddress          text ,
	foreign key (id) references people(id) ,    --is a relationship
	foreign key (billingAddress) references places(address) ,    --billingAddress relationship
	foreign key (homeAddress) references places(address)    --homeAddress relationship
);

create table organisers (
	id   serial ,
	primary key (id) ,
	ownerby       serial not null ,
	name         LongNameValue ,
	logo         bytea ,
	about        varchar ,
	pageColourProvideTheme      serial not null ,
	foreign key (ownerby) references users(id) ,    --owned by users relationship
	foreign key (pageColourProvideTheme) references pageColours(id)    -- has themem relationship
);

create table contactLists (
	id           serial ,
	ownedByUser           serial not null ,
	name                  LongNameValue ,
	primary key (id , name) ,
	foreign key (ownedByUser) references users(id)    -- user owns relationship
);

-- memberof relationship
create table memberOf (
    contactListID       serial  ,
    personID            serial  ,
    nickName            LongNameValue ,
    primary key (contactListID , personID) ,
    foreign key (contactListID) references contactLists(id) ,
    foreign key (personID ) references people(id)
);


-- EVENTS: things that happen and which people attend via tickets

create table eventInfo (
	id                      serial ,
	primary key (id)               ,
	hasTheme                serial not null ,
	oraganisedBy            serial  not null ,
	placeLocated            serial not null,
    showFee       boolean  default  false ,
    showLeft      boolean  default  false ,
    isPrivate     boolean  default  true ,
    title         varchar(100) ,
    details       text ,
    startingTime      date ,
    duration          interval ,
    foreign key (hasTheme) references pageColours(id) , --info for event info has theme relationship
    foreign key (oraganisedBy) references organisers(id) , --oraganised by organiser relationship
    foreign key (placeLocated) references places(id)  --located in place relationship
);

create table eventInfoCategories (
    eventInfoCategorieID             serial ,
    categorie                        text ,
    primary key (eventInfoCategorieID,categorie) ,
    foreign key (eventInfoCategorieID) references eventInfo(id)
);

create table events (
	id                       serial ,
	primary key (id)                ,
	eventInfoForm            serial  not null ,
    satrtData                date ,
    satrtTime                date ,
    foreign key (eventInfoForm ) references eventInfo (id)  ----- info for eventsinfo relationship
);

--invited To relation
create table invitedTo (
	eventInvitID            serial ,
	personInvitID           serial ,
	primary key (eventInvitID, personInvitID) ,
	foreign key (eventInvitID) references events(id) ,
    foreign key (personInvitID) references people(id)
);

--attended relation
create table attended (
	eventAttendID              serial ,
	personAttendID             serial ,
	primary key ( eventAttendID, personAttendID) ,
	foreign key (eventAttendID) references events(id) ,
    foreign key (personAttendID) references people(id)
);

create domain eventRepetitionType as varchar(10)
	check (value in ('daily','weekly','monthly-by-day','monthly-by-date'));

create domain dayOfWeekType as char(3)
	check (value in ('mon','tue','wed','thu','fri','sat','sun'));


create table repeatingEvents (
	id          serial ,
	primary key (id)   ,
	repeatingEventInform      serial not null ,
	lowerData                 date ,
	upperData                 date ,
	repeatType                eventRepetitionType ,
	foreign key (repeatingEventInform) references eventInfo (id)  ----- info for repeatingeventsinfo relationship
);

create table dailyEvents (
	dailyEventID          serial ,
	primary key (dailyEventID)  ,
	frequency           integer ,
	foreign key (dailyEventID ) references repeatingEvents (id)  ----- from RepeatingEvents
);

create table weeklyEvents (
	weeklyEventID          serial ,
	primary key (weeklyEventID) ,
	dayOfWeek              DayOfWeekType  ,
	frequency            integer ,
	foreign key (weeklyEventID ) references repeatingEvents (id)  ----- from RepeatingEvents
);

create table monthlyByDayEvents (
	MonthlyByDayEventID          serial ,
	primary key (MonthlyByDayEventID )  ,
	frequency              integer ,
	dayOfWeek        DayOfWeekType ,
	foreign key (MonthlyByDayEventID  ) references repeatingEvents (id)  ----- from RepeatingEvents
);

create table MonthlyByDateEvents (
	MonthlyByDateEventID          serial ,
	primary key (MonthlyByDateEventID  ) ,
	dayOfWeek              DayOfWeekType ,
	foreign key (MonthlyByDateEventID   ) references repeatingEvents (id)  ----- from RepeatingEvents
);


---- events instance of repeating event relationship

create table instanceOf (
    eventsInID                  serial ,
    repeatingEventsInID            serial ,
    primary key (eventsInID,repeatingEventsInID) ,
    foreign key (eventsInID) references events (id) ,
    foreign key (repeatingEventsInID) references repeatingEvents (repeatingEventID)
);


-- TICKETS: things that let you attend an event

create table ticketTypes (
	id         serial ,
	primary key (id)   ,
	forEventInfoID       serial not null,
	type                 LongNameValue ,
	description          text ,
	totalNumber          integer ,
	maxPerSale           integer ,
	currency             varchar(3) ,
	price                integer ,
	foreign key (forEventInfoID) references eventInfo (id)  --ticket type for event info relationship ??? 如何表达event info也全部参与
);

create table soldTickets (
    id      serial ,
    primary key (id) ,
    quantity          integer ,
    hasTicketType     serial not null,
    forEvent          serial not null,
    soldPerson        serial not null,
    foreign key (hasTicketType) references ticketTypes (id) ,  ----- has type tickettype relationship
    foreign key (forEvent ) references events (id) ,   -----sold for event relationship
    foreign key (soldPerson) references people (id)     ----- sold to person relationship
);
