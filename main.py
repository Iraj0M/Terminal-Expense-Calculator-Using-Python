from database import *
from rich.console import Console
from rich.table import Table
import matplotlib.pyplot as plt
console = Console()

Create_DB()

while True:
    console.print("\n[bold cyan]" + "=" * 100 + "[/bold cyan]")
    console.rule("[bold green]PERSONAL EXPENSE TRACKER[/bold green]")
    console.print("[bold cyan]" + "=" * 100 + "[/bold cyan]")

    console.print("[1]  Add Expense")
    console.print("[2]  View All Expenses")
    console.print("[3]  Delete Expense")
    console.print("[4]  Drop Database")
    console.print("[5]  Edit Expense")
    console.print("[6]  Show Total Expenses")
    console.print("[7]  Expense Pie Chart")
    console.print("[0]  Exit")

    ch = input("\nEnter your choice: ")

    # ADD EXPENSE
    if ch == '1':
        try:
            date = input("Enter Date (YYYY-MM-DD): ")
            amount = float(input("Enter Amount: "))

            if amount <= 0:
                console.print("[red]Amount must be greater than 0![/red]")
                continue

            category = input("Enter Category: ")
            desc = input("Enter Description: ")

            expense_add(date, amount, category, desc)

            console.print("[green]Expense Added Successfully![/green]")

        except ValueError:
            console.print("[red]Invalid Amount![/red]")

    # VIEW EXPENSES
    elif ch == '2':

        expenses = expense_view_all()

        if not expenses:
            console.print("[yellow]No expenses found.[/yellow]")
            continue

        table = Table(title="Expense Records")

        table.add_column("ID", style="cyan")
        table.add_column("Date", style="green")
        table.add_column("Amount", style="red")
        table.add_column("Category", style="yellow")
        table.add_column("Description", style="white")

        for exp in expenses:
            table.add_row(
                str(exp[0]),
                exp[1],
                f"₹{exp[2]:.2f}",
                exp[3],
                exp[4]
            )

        console.print(table)

    # DELETE EXPENSE
    elif ch == '3':

        try:
            expense_id = int(input("Enter Expense ID: "))

            if delete_expense(expense_id):
                console.print(
                    "[green]Expense Deleted Successfully![/green]"
                )
            else:
                console.print(
                    "[red]Expense ID not found![/red]"
                )

        except ValueError:
            console.print("[red]Invalid ID![/red]")

    # DROP DATABASE
    elif ch == '4':

        confirm = input(
            "Are you sure you want to delete ALL expenses? (yes/no): "
        )

        if confirm.lower() == "yes":
            drop_database()
            Create_DB()

            console.print(
                "[bold red]Database Dropped Successfully![/bold red]"
            )
        else:
            console.print("[yellow]Operation Cancelled.[/yellow]")

    # EDIT EXPENSE
    elif ch == '5':

        try:
            expense_id = int(input("Enter Expense ID: "))

            new_date = input("Enter New Date (YYYY-MM-DD): ")
            new_amount = float(input("Enter New Amount: "))

            if new_amount <= 0:
                console.print("[red]Amount must be greater than 0![/red]")
                continue

            new_category = input("Enter New Category: ")
            new_desc = input("Enter New Description: ")

            edit_expense(
                expense_id,
                new_date,
                new_amount,
                new_category,
                new_desc
            )

            console.print("[green]Expense Updated Successfully![/green]")

        except ValueError:
            console.print("[red]Invalid Input![/red]")

    # TOTAL EXPENSES
    elif ch == '6':

        total = total_expenses()

        console.print(
            f"\n[bold magenta]Total Expenses: ₹{total:.2f}[/bold magenta]"
        )
    elif ch == '7':

        data = expense_by_category()

        if not data:
            console.print("[red]No expense data found![/red]")
            continue

        categories = [row[0] for row in data]
        amounts = [row[1] for row in data]

        plt.figure(figsize=(8, 8))
        plt.pie(
            amounts,
            labels=categories,
            autopct='%1.1f%%'
        )

        plt.title("Expenses by Category")
        plt.show()
    # EXIT
    elif ch == '0':

        console.print(
            "\n[bold green]Thank you for using Expense Tracker![/bold green]"
        )
        break

    else:
        console.print("[red]Invalid Choice! Please Try Again.[/red]")