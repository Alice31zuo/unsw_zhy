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
    name        LongNameValue ,
    address     text ,
    city        LongNameValue,
    state       LongNameValue ,
    country     LongNameValue ,
    postalCode  integer ,
    gpsCoords   LocationValue ,
	primary key (id)
);


-- PAGEs: settings for pages in et.org

create table PageColours (
	id       serial,
	ownedBy            serial,
	maintext     text ,
	heading      LongNameValue,
	headtext     text ,
	borders      ColourValue ,
	boxes        ColourValue ,
	links        URLValue ,
	background   ColourValue ,
	isTemplate   boolean ,
	name         LongNameValue ,
	primary key (id)
)
alter table PageColours
    add foreign key (ownedBy) references Users(id) ;   --ownedby relationship


-- PEOPLE: information about various kinds of people
-- Users are People who can login to the system
-- Contacts are people about whom we have minimal info
-- Organisers are "entities" who organise Events

create table People (
	id     serial ,
	givenName    NameValue not null ,
	email        EmailValue not null ,
	familyName   NameValue ,
	primary key (id)
);

create table Users (
	id       serial ,
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
	foreign key (homeAddress) references Places(address) ,    --homeAddress relationship
	primary key (id)
);

create table Organisers (
	id   serial ,
	ownerby       serial not null ,
	name         LongNameValue ,
	logo         bytea ,
	about        varchar ,
	pageColourProvideTheme      serial not null ,
	foreign key (ownerby) references Users(id) ,    --owned by users relationship
	foreign key (pageColourProvideTheme) references PageColours(id) ,    -- has themem relationship
	primary key (id)
);

create table ContactLists (
	id           serial ,
	ownedByUser           serial not null ,
	name                  LongNameValue ,
	foreign key (ownedByUser) references Users(id) ,    -- user owns relationship
	primary key (id , name)
);

-- memberof relationship
create table MemberOf (
    contactListID       serial  ,
    personID            serial  ,
    nickName            LongNameValue ,
    foreign key (contactListID) references ContactLists(id) ,
    foreign key (personID ) references People(id) ,
    primary key (contactListID , personID)
);


-- EVENTS: things that happen and which people attend via tickets

create table EventInfo (
	id                      serial ,
	hasTheme                serial not null ,
	oraganisedBy            serial  not null ,
	placeLocated            serial not null,
    showFee       boolean  default  0,
    showLeft      boolean  default  0,
    isPrivate     boolean  default  1,
    title         varchar(100) ,
    details       text ,
    startingTime      date ,
    duration          interval ,
    foreign key (hasTheme) references PageColours(id) , --info for event info has theme relationship
    foreign key (oraganisedBy) references Organisers(id) , --oraganised by organiser relationship
    foreign key (placeLocated) references Places(id) , --located in place relationship
    primary key (id)
);

create table EventInfoCategories (
    eventInfoCategorieID             serial ,
    categorie                        text ,
    foreign key (eventInfoCategorieID) references EventInfo(id),
    primary key (eventInfoCategorieID,categorie)
);

create table Events (
	id                       serial ,
	eventInfoForm            serial  not null ,
    satrtData                data ,
    satrtTime                data ,
    foreign key (eventInfoForm ) references EventInfo (id) , ----- info for eventsinfo relationship
	primary key (id)
);

--invited To relation
create table InvitedTo (
	eventInvitID            serial ,
	personInvitID           serial ,
	foreign key (eventInvitID) references Events(id) ,
    foreign key (personInvitID) references People(id) ,
	primary key (eventInvitID, personInvitID)
);

--attended relation
create table Attended (
	eventAttendID              serial ,
	personAttendID             serial ,
	foreign key (eventAttendID) references Events(id) ,
    foreign key (personAttendID) references People(id) ,
	primary key ( eventAttendID, personAttendID)
);

create domain EventRepetitionType as varchar(10)
	check (value in ('daily','weekly','monthly-by-day','monthly-by-date'));

create domain DayOfWeekType as char(3)
	check (value in ('mon','tue','wed','thu','fri','sat','sun'));


create table RepeatingEvents (
	id          serial ,
	repeatingEventInform      serial not null ,
	lowerData                 data ,
	upperData                 data ,
	repeatType                EventRepetitionType ,
	foreign key (repeatingEventInform) references EventInfo (id) , ----- info for repeatingeventsinfo relationship
	primary key (id)
);

create table DailyEvents (
	dailyEventID          serial ,
	frequency           integer ,
	foreign key (dailyEventID ) references RepeatingEvents (id) , ----- from RepeatingEvents
	primary key (dailyEventID)
);

create table WeeklyEvents (
	weeklyEventID          serial ,
	dayOfWeek              DayOfWeekType  ,
	frequency            integer ,
	foreign key (weeklyEventID ) references RepeatingEvents (id) , ----- from RepeatingEvents
	primary key (weeklyEventID)
);

create table MonthlyByDayEvents (
	MonthlyByDayEventID          serial ,
	frequency              integer ,
	dayOfWeek        DayOfWeekType ,
	foreign key (MonthlyByDayEventID  ) references RepeatingEvents (id) , ----- from RepeatingEvents
	primary key (MonthlyByDayEventID )
);

create table MonthlyByDateEvents (
	MonthlyByDateEventID          serial ,
	dayOfWeek              DayOfWeekType ,
	foreign key (MonthlyByDateEventID   ) references RepeatingEvents (id) , ----- from RepeatingEvents
	primary key (MonthlyByDateEventID  )
);


---- events instance of repeating event relationship

create table InstanceOf (
    eventsInID                  serial ,
    repeatingEventsInID            serial ,
    foreign key (eventsInID) references Events (id) ,
    foreign key (repeatingEventsInID) references RepeatingEvents (repeatingEventID) ,
    primary key (eventsInID,repeatingEventsInID)
);


-- TICKETS: things that let you attend an event

create table TicketTypes (
	id         serial ,
	forEventInfoID       serial not null,
	type                 LongNameValue ,
	description          text ,
	totalNumber          integer ,
	maxPerSale           integer ,
	currency             varchar(3) ,
	price                integer ,
	foreign key (forEventInfoID) references EventInfo (id) , --ticket type for event info relationship ??? 如何表达event info也全部参与
	primary key (id)
);

create table SoldTickets (
    id      serial ,
    quantity          integer ,
    hasTicketType     serial not null,
    forEvent          serial not null,
    soldPerson        serial not null,
    foreign key (hasTicketType) references TicketTypes (id) ,  ----- has type tickettype relationship
    foreign key (forEvent ) references Events (id) ,   -----sold for event relationship
    foreign key (soldPerson) references People (id) ,    ----- sold to person relationship
    primary key (id)
);
