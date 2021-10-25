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

create table Places (
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

create table PageColours (
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
alter table PageColours
    add foreign key (ownedBy) references Users(id) ;   --ownedby relationship


-- PEOPLE: information about various kinds of people
-- Users are People who can login to the system
-- Contacts are people about whom we have minimal info
-- Organisers are "entities" who organise Events

create table People (
	id     serial ,
	primary key (id) ,
	givenName    NameValue not null ,
	email        EmailValue not null ,
	familyName   NameValue
);

create table Users (
	id       serial ,
	primary key (id) ,
	gender       GenderValue ,
	birthday     date ,
	phone        integer ,
	blog         URLValue ,
	showName     LongNameValue ,
	password     varchar(30) not null,
	website      URLValue ,
	billingAddress       text not null ,
	homeAddress          text ,
	foreign key (id) references People(id) ,    --is a relationship
	foreign key (billingAddress) references Places(address) ,    --billingAddress relationship
	foreign key (homeAddress) references Places(address)    --homeAddress relationship
);

create table Organisers (
	id   serial ,
	primary key (id)
	ownerby       serial not null ,
	name         LongNameValue ,
	logo         bytea ,
	about        varchar ,
	pageColourProvideTheme      serial not null ,
	foreign key (ownerby) references Users(id) ,    --owned by users relationship
	foreign key (pageColourProvideTheme) references PageColours(id)    -- has themem relationship
);

create table ContactLists (
	id           serial ,
	ownedByUser           serial not null ,
	name                  LongNameValue ,
	primary key (id , name) ,
	foreign key (ownedByUser) references Users(id)    -- user owns relationship
);

-- memberof relationship
create table MemberOf (
    contactListID       serial  ,
    personID            serial  ,
    nickName            LongNameValue ,
    primary key (contactListID , personID) ,
    foreign key (contactListID) references ContactLists(id) ,
    foreign key (personID ) references People(id)
);


-- EVENTS: things that happen and which people attend via tickets

create table EventInfo (
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
    foreign key (hasTheme) references PageColours(id) , --info for event info has theme relationship
    foreign key (oraganisedBy) references Organisers(id) , --oraganised by organiser relationship
    foreign key (placeLocated) references Places(id)  --located in place relationship
);

create table EventInfoCategories (
    eventInfoCategorieID             serial ,
    categorie                        text ,
    primary key (eventInfoCategorieID,categorie)
    foreign key (eventInfoCategorieID) references EventInfo(id)
);

create table Events (
	id                       serial ,
	primary key (id)                ,
	eventInfoForm            serial  not null ,
    satrtData                data ,
    satrtTime                data ,
    foreign key (eventInfoForm ) references EventInfo (id)  ----- info for eventsinfo relationship
);

--invited To relation
create table InvitedTo (
	eventInvitID            serial ,
	personInvitID           serial ,
	primary key (eventInvitID, personInvitID) ,
	foreign key (eventInvitID) references Events(id) ,
    foreign key (personInvitID) references People(id)
);

--attended relation
create table Attended (
	eventAttendID              serial ,
	personAttendID             serial ,
	primary key ( eventAttendID, personAttendID) ,
	foreign key (eventAttendID) references Events(id) ,
    foreign key (personAttendID) references People(id)
);

create domain EventRepetitionType as varchar(10)
	check (value in ('daily','weekly','monthly-by-day','monthly-by-date'));

create domain DayOfWeekType as char(3)
	check (value in ('mon','tue','wed','thu','fri','sat','sun'));


create table RepeatingEvents (
	id          serial ,
	primary key (id)   ,
	repeatingEventInform      serial not null ,
	lowerData                 data ,
	upperData                 data ,
	repeatType                EventRepetitionType ,
	foreign key (repeatingEventInform) references EventInfo (id) , ----- info for repeatingeventsinfo relationship
);

create table DailyEvents (
	dailyEventID          serial ,
	primary key (dailyEventID)  ,
	frequency           integer ,
	foreign key (dailyEventID ) references RepeatingEvents (id)  ----- from RepeatingEvents
);

create table WeeklyEvents (
	weeklyEventID          serial ,
	primary key (weeklyEventID) ,
	dayOfWeek              DayOfWeekType  ,
	frequency            integer ,
	foreign key (weeklyEventID ) references RepeatingEvents (id)  ----- from RepeatingEvents
);

create table MonthlyByDayEvents (
	MonthlyByDayEventID          serial ,
	primary key (MonthlyByDayEventID )  ,
	frequency              integer ,
	dayOfWeek        DayOfWeekType ,
	foreign key (MonthlyByDayEventID  ) references RepeatingEvents (id)  ----- from RepeatingEvents
);

create table MonthlyByDateEvents (
	MonthlyByDateEventID          serial ,
	primary key (MonthlyByDateEventID  ) ,
	dayOfWeek              DayOfWeekType ,
	foreign key (MonthlyByDateEventID   ) references RepeatingEvents (id)  ----- from RepeatingEvents
);


---- events instance of repeating event relationship

create table InstanceOf (
    eventsInID                  serial ,
    repeatingEventsInID            serial ,
    primary key (eventsInID,repeatingEventsInID) ,
    foreign key (eventsInID) references Events (id) ,
    foreign key (repeatingEventsInID) references RepeatingEvents (repeatingEventID)
);


-- TICKETS: things that let you attend an event

create table TicketTypes (
	id         serial ,
	primary key (id)   ,
	forEventInfoID       serial not null,
	type                 LongNameValue ,
	description          text ,
	totalNumber          integer ,
	maxPerSale           integer ,
	currency             varchar(3) ,
	price                integer ,
	foreign key (forEventInfoID) references EventInfo (id)  --ticket type for event info relationship ??? 如何表达event info也全部参与
);

create table SoldTickets (
    id      serial ,
    primary key (id) ,
    quantity          integer ,
    hasTicketType     serial not null,
    forEvent          serial not null,
    soldPerson        serial not null,
    foreign key (hasTicketType) references TicketTypes (id) ,  ----- has type tickettype relationship
    foreign key (forEvent ) references Events (id) ,   -----sold for event relationship
    foreign key (soldPerson) references People (id)     ----- sold to person relationship
);
