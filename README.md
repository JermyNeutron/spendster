# Spendster
A quick way to scrape your bank and credit card statements for your own personal tracking.

>[!WARNING]
> As of 06/27/2024, these are the only supported statements:
>
> **Checking Accounts**
> - Chase Checking (+2 transaction pages)
> - SchoolsFirst Credit Union Checking (1 page)
>
> **Credit Cards**
> - Chase Sapphire Preferred (+2 transaction pages, card payments/credits not included)
> - SchoolsFirst Credit Union Inspire (1 page)
> - Synchrony Car Care (1 page)
> - (**WIP**) PayPal Credit
>
> This will be updated as additional statements and institutions are prepared. 

## Setup
None. Simply launch the .exe.

## Usage
Drag and drop your checking or credit card statement into the prompt to create a comma-separated values (CSV) file (currently a temp file located 'temp/temp.csv'). It will automatically copy the contents of the CSV into your clipboard so once you drag and drop your chosen statement, you can go into any spreadsheet and press \<CTRL + V\>. You can also open and view the CSV file with any spread sheet viewer or upload online to Google Sheets to view. After the program instantly scrapes the statement, you can continue to drag and drop one statement at a time.
To exit the program, enter 'q' or just click the 'X' on the top right.

## Frequently Asked Questions
### Can I attach multiple documents at a time?
Not at this time. This program can only filter one document at a time.

## References

### Libraries
- pdfminer.six
- pyperclip

### Github
Visit https://github.com/JermyNeutron/spendster