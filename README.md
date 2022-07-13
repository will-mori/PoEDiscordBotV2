# PoEDiscordBotV2
A spiritual successor to my earlier [PCBot](https://github.com/wmoriUCI/PCBot).  The original PCBot made use of PoE's API to query trade items.  Since the last commit to that repo, I took some classes and was inspired to transition the bot to use a multithreaded approach instead over the ansync model that Discord initially provided.  However due to needing to maintain the async model and Python's GIL, the result was clunky, less efficient, and I was ultimately unhappy with the result.  Sometime after this, PoE changed how private parties are allowed to access their API requiring a dev application, rate limits, and many other things.  For these reasons the original PCBot has been made defunct.

PoEDiscordBotV2 rises from the ashes of PCBot making use of [@maximumstock](https://github.com/maximumstock)'s [poe-stash-indexer](https://github.com/maximumstock/poe-stash-indexer/tree/master/trade-api).  This user has created a REST-like API and hosts it for others to query on.  This means PCBot is no longer price checking items and is instead a bot to query exchange rates
## Functionality
The main command to use is '!query'.  This command respond with a message listing out the various conversion rates along with the total purchasable stock and freshness of the listings(Future implementation).  This command in the interim will output each returned listing to the terminal.  This command can be used in the following forms:
1. '!query {currency}' to see generic listings of the currency using the default listing limit
2. '!query {currency} {currency}' to see listings of the first currency using the second currency using the default listing limit
3. '!query {currency} {limit}' to see generic listings with the number of listings limited by limit
4. '!query {currency} {currency} {limit}' to see listings of the first currencyto be purchased with the second currency with the number of listings limited by limit

A secondary command more useful for data logging is !log-currency.  This function write to file the conversion rates for Chaos Orbs to Exalted Orbs, Exalted Orbs to Mirrors of Kalandra, Exalted Orbs to Awakener's Orbs, and Exalted Orbs to Ancient Orbs.  In the future, this function may be scrapped or made into it's on project to generate a dataset on listings.

There are some other debugging and support commands that are accessible to the user, but these commands implement no interesting functionality
