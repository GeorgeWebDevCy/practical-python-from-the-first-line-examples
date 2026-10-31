class LoanItem:
    def __init__(self, title):
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Title is required")
        self.title = title.strip()
        self.borrower = None

    def checkout(self, borrower):
        if not isinstance(borrower, str) or not borrower.strip():
            raise ValueError("Borrower is required")
        if self.borrower is not None:
            raise ValueError("Item is already borrowed")
        self.borrower = borrower.strip()

    def return_item(self):
        if self.borrower is None:
            raise ValueError("Item is not borrowed")
        self.borrower = None

    def status(self):
        if self.borrower is None:
            return f"{self.title}: available"
        return f"{self.title}: borrowed by {self.borrower}"


if __name__ == "__main__":
    item = LoanItem("Field guide")
    print(item.status())
    item.checkout("Sam")
    print(item.status())
    item.return_item()
    print(item.status())
