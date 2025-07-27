# Inventory Logger
Welcome to a personal passion project!
Having spent a few years in retail arbitrage, and over a decade in collecting odds and ends
I have decided to create a Python program that allows me to take inventory
of all the stuff I have amassed.  From Sneakers, to Vinyl, CD's, and an assortment
of other collectibles, I needed a fool-proof way to track what I own, as well
as how much I spent, and how much it was worth! 

A cross-category inventory management app built with **Python**, **Tkinter**, and **Supabase**. It supports user login, data entry (sneakers, media, collectibles), local CSV storage, and cloud storage in Supabase—with Row-Level Security (RLS) per user.

---

## 🚀 Features

* **Tkinter + TTK-Themes UI**: User-friendly tabbed forms for sneakers, media, collectibles, and spreadsheet.
* **Supabase Authentication & Database**: Secure user login, per-user data isolation, and persistent cloud storage.
* **Local CSV Backup**: Optionally logs data to local CSV files per category (`.csv` files).
* **Row-Level Security**: Ensures users can only access their own data.(In Progress)
* **Spreadsheet View**: Combined table view in the app UI with filtering.

---

## 📁 Project Structure

```
inventory-logger/
├── src/logger/
│   ├── gui_scratch.py
│   ├── sneaker_inventory_log.py
│   ├── media_inventory_log.py
│   ├── collectibles_inventory_log.py
│   ├── data_handling.py
│   └── supabase_client.py
└── README.md
```

* **`gui_scratch.py`**: Main application UI implementation.
* **`*_inventory_log.py`**: Domain logic and dataclass definitions for each category.
* **`data_handling.py`**: Local CSV persistence.
* **`supabase_client.py`**: Initializes Supabase client using environment settings.

---

## 🎯 Prerequisites

* Python 3.10+
* Virtual environment (e.g. `venv`)
* Install dependencies:

```bash
pip install pandas ttkthemes supabase py-dotenv
```

* A Supabase project configured with:

  * Tables: `sneakers`, `media`, `collectibles`
  * Columns include `user_id` and matching fields
  * RLS enabled and policies set to allow inserts/reads for the correct user:

```sql
-- Example for sneakers
CREATE POLICY "Insert sneakers for owner"
ON public.sneakers
FOR INSERT
TO authenticated
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Select sneakers for owner"
ON public.sneakers
FOR SELECT
TO authenticated
USING (auth.uid() = user_id);
```

---

## ⚙️ Configuration

1. Copy `.env.example` to `.env` with your Supabase values:

```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-secret
```

2. Load environment variables before running (e.g. via `python-dotenv`).

---

## 🧺 Usage

### Run the app:

```bash
cd src/logger
python gui_scratch.py
```

* Login tab is shown first.
* After login, data entry tabs are unlocked and live Supabase CRUD operations begin.
* Submitted entries are saved both locally (CSV) and in Supabase.
* Use the "Spreadsheet" tab to view all saved entries and export to CSV.

---

## 📥 Local CSV Logging

* Rows are appended per category with a "Total Profit" summary row at the end.
* CSV files are stored in the working directory:

  * `sneaker_inventory_log.csv`
  * `media_inventory_log.csv`
  * `collectibles_inventory_log.csv`
* When appending, the old summary row is removed and recalculated.

---

## 📅 Data Loading (on start / login)

* On successful login, previously saved entries (filtered by `user_id`) are fetched from Supabase.
* In-memory data list is populated and the Treeview UI is refreshed.

---

## 🧪 Testing

* Unit tests available (if included), e.g.:

```bash
python -m unittest discover
```

* Focus on dataclass behavior, profit calculations, and Supabase insert logic.

---

## 🧹 Customization Ideas

* Add support for **editing/deleting** entries.
* Include **filter dropdowns** per category in UI.
* Visualize profits over time using Matplotlib/Plotly.
* Extend to other inventory categories.

---

Built by **strangeco0l** 

