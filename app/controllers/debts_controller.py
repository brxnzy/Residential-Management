from datetime import datetime
from config.database import connection_db
from apscheduler.schedulers.background import BackgroundScheduler

class Debts:
    def __init__(self):
        self.db = connection_db()
        self.db.autocommit = True
        self.scheduler = BackgroundScheduler()
        # self.scheduler.add_job(self.generate_monthly_debts, 'interval', minutes=1)
        self.scheduler.add_job(self.generate_monthly_debts, 'cron', day=1, hour=0, minute=0)

        self.scheduler.start()

    def generate_monthly_debts(self):
        try:
            cursor = self.db.cursor(dictionary=True, buffered=True)  # Buffered para evitar errores

            # Obtener el monto actual de la deuda
            cursor.execute("SELECT amount FROM debt_amount")
            result = cursor.fetchone()
            if not result:
                print("No hay un monto establecido en debt_amount.")
                cursor.close()
                return False
            amount = result['amount']

            # Obtener todos los usuarios con el rol 'resident'
            cursor.execute("""
                SELECT ur.user_id
                FROM user_roles ur
                JOIN roles r ON ur.role_id = r.id
                WHERE r.name = 'resident'
            """)
            users = cursor.fetchall()

            now = datetime.now()
            year = now.year
            month = now.month
            nuevas_deudas = 0

            for user in users:
                user_id = user['user_id']

                # Verificar si ya existe deuda en ese mes para ese usuario
                cursor.execute("""
                    SELECT 1 FROM debts
                    WHERE id_usuario = %s AND period = %s AND month = %s
                """, (user_id, year, month))
                exists = cursor.fetchone()
                if exists:
                    continue  # Ya tiene deuda este mes, no se inserta

                # Insertar nueva deuda
                cursor.execute("""
                    INSERT INTO debts (id_usuario, amount, period, month)
                    VALUES (%s, %s, %s, %s)
                """, (user_id, amount, year, month))
                nuevas_deudas += 1

            print(f"✅ Se generaron {nuevas_deudas} nuevas deudas en {month}/{year}")
            cursor.close()
            return True

        except Exception as e:
            print(f"❌ Error al generar deudas mensuales: {e}")
            self.db.rollback()
            try:
                cursor.close()
            except:
                pass
            return False

    
    def get_debs(self):
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT * FROM debts")
            debts = cursor.fetchall()
            cursor.close()
            return debts
        except Exception as e:
            print(e)
            return False
        
    
    def get_users_debts(self, user_id):
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM debts WHERE id_usuario = %s", (user_id,))
            debts = cursor.fetchall()
            cursor.close()
            print(debts)
            return debts
        except Exception as e:
            print(e)
            return False
        
    def get_debtors(self):
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("""
            SELECT 
                    u.id AS user_id,
                    CONCAT(u.name, ' ', u.last_name) AS resident,
                    d.amount AS debt_amount,
                    d.period,
                    d.month,
                    d.id,
                    COALESCE(
                        CONCAT( a.building, ', Apto. ', a.apartment_number),
                        CONCAT('Casa ', h.house_number)
                    ) AS residence
                FROM debts d
                JOIN users u ON u.id = d.id_usuario
                LEFT JOIN apartments a ON a.id_usuario = d.id_usuario
                LEFT JOIN houses h ON h.id_usuario = d.id_usuario
                WHERE d.amount > 0;
                """)
            debtors = cursor.fetchall()
            cursor.close()
            return debtors
        except Exception as e:
            print(e)
            return False    
        
    def get_debt_amount(self):
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("""
                SELECT amount from debt_amount limit 1;
            """)
            debt_amount = cursor.fetchone()
            cursor.close()
            return debt_amount
        
        except Exception as e:
            print(f"error tomando el debt amount",e)
            return False
    
    def update_debt_amount(self,amount):
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("""
                UPDATE debt_amount SET amount = %s;
            """,(amount,))
            self.db.commit()
            cursor.close()
            return True
        
        except Exception as e:
            print(f"error actualizando el debt amount",e)
            return False
        
    def generate_debt(self, user_id):
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("""
            select amount from debt_amount;
            """)
            amount = cursor.fetchone()
            amount = amount['amount']
            now = datetime.now()
            month = now.month
            year = now.year
            cursor.execute("""
                INSERT INTO debts (id_usuario, amount, period, month) VALUES (%s, %s, %s, %s);
            """,(user_id, amount, year, month))
            return True
        except Exception as e:
            print(f"error generando la deuda",e)
            return False