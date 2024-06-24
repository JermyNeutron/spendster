# Spendster
A quick way to scrape your bank and credit card statements for your own personal tracking.

>[!WARNING]
> As of 06/23/2024, these are the only supported statements:
>
> **Checking Accounts**
> - Chase Checking (+2 transaction pages)
> - SchoolsFirst Credit Union Checking (1 page)
>
> **Credit Cards**
> - Chase Sapphire Preferred (+2 transaction pages, card payments/credits not included)
> - (**WIP**) SchoolsFirst Credit Union Inspire
> - (**Planned**) Synchrony Car Care
>
> This will be updated as additional statements and institutions are prepared. 

<!-- ## Setup -->

## Usage
Drag and drop your checking or credit card statement into the prompt to create a comma-separated values (CSV) file. It will automatically copy the contents of the CSV into your clipboard so once you drag and drop your bank statement, you can go into spreadsheet and press \<CTRL + V\>. You can also open and view the CSV file with any spread sheet viewer or upload online to Google Sheets to view.

<!-- ## Frequently Asked Questions -->

## References

### Libraries
- pdfminer.six
- pyperclip

### Github
Visit https://github.com/JermyNeutron/spendster