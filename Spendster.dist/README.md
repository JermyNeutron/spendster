# Spendster
A quick way to scrape your bank and credit card statements for your own personal tracking.

>[!WARNING]
> As of 07/25/2024, these are the only supported statements:
>
> **Checking Accounts**
> - Chase Checking (+2 transaction pages)
> - SchoolsFirst Credit Union Checking (1 page)
>
> **Credit Cards**
> - Chase Sapphire Preferred (+2 transaction pages, card payments/credits not included)
> - PayPal Credit (1 page)
> - SchoolsFirst Credit Union Inspire (1 page)
> - Synchrony Car Care (1 page)
>
> This will be updated as additional statements and institutions are prepared. 

## Setup
None. Simply launch the Spendster.exe from the Spendster.dist/ folder.

## Usage
Drag your checking or credit card statement into the prompt to create a comma-separated values (CSV) file (currently a temp file located 'temp/temp.csv'). It will automatically copy the contents of the CSV into your clipboard so once you drag your chosen statement and hit \<ENTER\>, you can go into any spreadsheet and press \<CTRL + V\> to paste the information. You can also open and view the CSV file with any spreadsheet viewer or upload online to Google Sheets to view. After the program instantly scrapes the statement, you can continue to drag additional statements one at a time.
To exit the program, enter 'q' or just click the 'X' on the top right.

You can currently enable TEST mode to see the print statements that help me troubleshoot issues by entering 'test' into the CLI. Check it out!

## Frequently Asked Questions
### Can I attach multiple documents at a time?
Not at this time. This program can only filter one document at a time.

## References

### Libraries
- pdfminer.six
- PyPDF2
- pyperclip

### Github
Visit https://github.com/JermyNeutron/spendster