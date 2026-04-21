\c demo
CREATE TABLE bookings.mart_route_sales AS
WITH route_agg AS (
    SELECT
        f.route_no,
        COUNT(DISTINCT s.flight_id) AS flights_count,
        COUNT(s.ticket_no) AS tickets_count,
        ROUND(AVG(s.price)::numeric, 2) AS avg_price,
        SUM(s.price) AS total_revenue,
        MIN(s.price) AS min_price,
        MAX(s.price) AS max_price
    FROM bookings.flights f
    LEFT JOIN bookings.segments s ON f.flight_id = s.flight_id
    GROUP BY f.route_no
)
SELECT
    r.route_no,
    r.departure_airport,
    r.arrival_airport,
    dep.city->>'en' AS dep_city,
    dep.country->>'en' AS dep_country,
    arr.city->>'en' AS arr_city,
    arr.country->>'en' AS arr_country,
    ra.flights_count,
    ra.tickets_count,
    ra.avg_price,
    ra.total_revenue,
    ra.min_price,
    ra.max_price
FROM (SELECT DISTINCT route_no, departure_airport, arrival_airport FROM bookings.routes) r
LEFT JOIN route_agg ra ON r.route_no = ra.route_no
LEFT JOIN bookings.airports_data dep ON r.departure_airport = dep.airport_code
LEFT JOIN bookings.airports_data arr ON r.arrival_airport = arr.airport_code
