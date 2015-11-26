# Swiss-Tournament
Used Python DB API and a PostgreSQL database server to keep track of players and matches in a swiss style game tournament.

<b>Technologies used: </b>
<li> Python DB API - psycopg2 </li>
<li> Database - PostgreSQL </li>
<li> VMWare Integration- vagrant </li>

<b> Fuctionalities: </b>
<li> Registration of players to the tournament </li>
<li> Removal of players from the tournament </li>
<li> Recording the results of matches between players </li>
<li> Creating the next round of matches based on the swiss style tournament rules </li>
<li> Handle draws by awarding half the points to each team </li>
<li> Handle odd number of teams by providing the weakest team a bye </li>

To run the application, use the following commands:
<li> <b> To get to the PostgreSQL command line util: </b> psql </li>
<li> <b> To create the database schema: </b> \i tournament.sql </li>
<li> <b> To run the given unit tests: </b> python tournament_test.py </li>

