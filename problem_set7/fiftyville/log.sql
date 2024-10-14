-- Keep a log of any SQL queries you execute as you solve the mystery.
select * from crime_scene_reports
where street = 'Humphrey Street';
--Bakery Witness--
select * from interviews
where transcript LIKE '%bakery%';
--witness 1 ruth--
select * from bakery_security_logs where year=2021 and month=7 and day=28 and hour=10 and minute between 15 and 25;
--check against licenses plates--
select p.name,bsl.activity,bsl.license_plate,bsl.year,bsl.month,bsl.day,bsl.hour,bsl.minute
from bakery_security_logs bsl
join people p on p.license_plate=bsl.license_plate
where bsl.year=2021 and bsl.month=7 and bsl.day=28 and bsl.hour=10 and bsl.minute between 15 and 25;
--check witness 2 re: atm--
select * from atm_transactions
where atm_location='Leggett Street'
and year=2021 and month =7 and day=28;
--add name of withdraws for atm--
select a.*,p.name
from atm_transactions a
join bank_accounts b on a.account_number=b.account_number
join people p on b.person_id=p.id
where a.atm_location='Leggett Street' and a.year=2021 and a.month=7 and a.day=28 and a.transaction_type='withdraw';
--witness 3 phone call investigation--
select *
from phone_calls
where year=2021 and month=7 and day=28 and duration<60;
--add names to call list of callers--
select p.name,pc.caller,pc.receiver,pc.year,pc.month,pc.day,pc.duration
from phone_calls pc
join people p on pc.caller=p.phone_number
where pc.year=2021 and pc.month=7 and pc.day=28 and pc.duration<60;
--explore airport to find fiftyville--
select * from airports;
--found fiftyville id (8) explore flights out)--
select f.*, origin.full_name as origin_airport, destination.full_name as destination_airport
from flights f
join airports origin on f.origin_airport_id=origin.id
join airports destination on f.destination_airport_id=destination.id
where origin.id=8 and f.year=2021 and f.month=7 and f.day=29
order by f.hour,f.minute;
--combine info from all three testimonies--
select p.name
from bakery_security_logs bsl
join people p on p.license_plate = bsl.license_plate
join bank_accounts ba on ba.person_id=p.id
join atm_transactions at on at.account_number=ba.account_number
join phone_calls pc on pc.caller=p.phone_number
where bsl.year=2021 and bsl.month=7 and bsl.day=28 and bsl.hour=10 and bsl.minute between 15 and 25
and at.atm_location='Leggett Street' and at.year=2021 and at.month=7 and at.day=28 and at.transaction_type='withdraw'
and pc.year=2021 and pc.month- 7 and pc.day=28 and pc.duration<60;
--narrow down from bruce/diana who is on flight--
select p.name
from people p
join passengers ps on p.passport_number=ps.passport_number
where ps.flight_id=36
and p.name in ('Bruce','Diana');
--who did bruce call--
select p2.name as receiver
from phone_calls pc
join people p1 on pc.caller=p1.phone_number
join people p2 on pc.receiver =p2.phone_number
where p1.name='Bruce' and pc.year=2021 and pc.month=7 and pc.day=28 and pc.duration<60;

