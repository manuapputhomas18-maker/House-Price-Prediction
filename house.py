# HOUSE PRICE PREDICTION PROJECT

# ========= IMPORT LIBRARIES =========

import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# ========= CONNECT TO MYSQL =========

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="house_db"
)

print("✅ MySQL Connected Successfully")

cursor = conn.cursor()

# ========= CREATE TABLE =========

cursor.execute("""
CREATE TABLE IF NOT EXISTS house (
    id INT AUTO_INCREMENT PRIMARY KEY,
    area FLOAT,
    bedroom INT,
    bathroom INT,
    price FLOAT
)
""")

conn.commit()

# ========= INSERT SAMPLE DATA =========

cursor.execute("SELECT COUNT(*) FROM house")

count = cursor.fetchone()[0]

# Insert data only if table is empty
if count == 0:

    cursor.execute("""
    INSERT INTO house(area, bedroom, bathroom, price)
    VALUES
    (1000, 2, 1, 3000000),
    (1200, 3, 2, 4500000),
    (1500, 3, 2, 5000000),
    (1800, 4, 3, 6500000),
    (2000, 4, 3, 7000000)
    """)

    conn.commit()

    print("✅ Sample Data Inserted")

# ========= FETCH DATA =========

cursor.execute(
    "SELECT area, bedroom, bathroom, price FROM house"
)

data = cursor.fetchall()

# ========= CREATE DATAFRAME =========

df = pd.DataFrame(
    data,
    columns=['area', 'bedroom', 'bathroom', 'price']
)

print("\n=========== DATASET ===========\n")

print(df)

# ========= VISUALIZATION =========

plt.scatter(df['area'], df['price'])

plt.xlabel("Area")

plt.ylabel("Price")

plt.title("House Price Prediction")

plt.show()

# ========= PREPARE DATA =========

X = df[['area', 'bedroom', 'bathroom']]

y = df['price']

# ========= SPLIT DATA =========

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.4,
    random_state=42
)
# ========= TRAIN MODEL =========

model = LinearRegression()

model.fit(X_train, y_train)

print("\n✅ Model Trained Successfully")

# ========= MAKE PREDICTION =========

predictions = model.predict(X_test)


print("\n=========== PREDICTIONS ===========\n")

for actual, predicted in zip(y_test, predictions):

    print("Actual Price :", actual)

    print("Predicted Price :", predicted)

    print()

# ========= CHECK ACCURACY =========

score = r2_score(y_test, predictions)

print("R2 Score :", score)

# ========= USER INPUT =========

print("\n=========== NEW HOUSE PREDICTION ===========")

area = float(input("Enter Area : "))

bedroom = int(input("Enter Bedrooms : "))

bathroom = int(input("Enter Bathrooms : "))

new_house = [[area, bedroom, bathroom]]

new_price = model.predict(new_house)

print(f"Predicted Price : ₹ {predicted:.2f}")

print("₹", new_price[0])

# ========= CLOSE CONNECTION =========

cursor.close()

conn.close()

print("\n✅ MySQL Connection Closed")