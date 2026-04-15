# class untuk item senjata
class Item:
    def __init__(self, name, damage):
        self.name = name
        self.damage = damage

# class untuk hero
class Hero:
    def __init__(self, name, attack_power):
        self.name = name
        self.attack_power = attack_power
        self.hp = 300
        self.item = None # set none di awal sblm pasang item

    # method untuk masang item
    def set_item(self, item):
        self.item = item

    # memotong hp hero dan cegah minus
    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    # method bawaan untuk menyerang
    def attack(self, enemy):
        # damage awal ambil dr base hero
        total_damage = self.attack_power
        nama_senjata = "Tangan Kosong"
        
        # tambah damage kalo pake senjata
        if self.item is not None:
            total_damage += self.item.damage
            nama_senjata = self.item.name
            
        # panggil method musuh (polymorphism)
        enemy.take_damage(total_damage, self, nama_senjata)

# parent class musuh
class Enemy:
    def __init__(self, name, hp):
        self.name = name
        self.hp = hp

    # method kosong buat dioverride
    def take_damage(self, damage, hero, weapon_name):
        pass

# musuh biasa tanpa shield
class BasicEnemy(Enemy):
    # terima damage murni
    def take_damage(self, damage, hero, weapon_name):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0
            
        print(f"{hero.name} menyerang {self.name} dengan {weapon_name} sebesar {damage} HP {self.name} sekarang {self.hp}")

# musuh pakai shield 30
class ShieldEnemy(Enemy):
    def take_damage(self, damage, hero, weapon_name):
        # potong damage base pakai shield 30
        damage_akhir = damage - 30
        
        # cegah minus biar ga nambah hp
        if damage_akhir < 0:
            damage_akhir = 0
            
        print(f"{self.name} mengaktifkan shield! Damage berkurang menjadi {damage_akhir}")
        
        self.hp -= damage_akhir
        if self.hp < 0:
            self.hp = 0
            
        print(f"{hero.name} menyerang {self.name} dengan {weapon_name} sebesar {damage_akhir} HP {self.name} sekarang {self.hp}")

# bos musuh (shield 40, attack 50)
class BossEnemy(Enemy):
    def take_damage(self, damage, hero, weapon_name):
        damage_akhir = damage - 40
        if damage_akhir < 0:
            damage_akhir = 0
            
        print(f"{self.name} mengaktifkan shield! Damage berkurang menjadi {damage_akhir}")
        
        self.hp -= damage_akhir
        if self.hp < 0:
            self.hp = 0
            
        print(f"{hero.name} menyerang {self.name} dengan {weapon_name} sebesar {damage_akhir} HP {self.name} sekarang {self.hp}")
        
        # bos otomatis counter kalo msh hidup
        if self.hp > 0:
            hero.take_damage(50)
            print(f"{self.name} menyerang balik {hero.name} sebesar 50")
            print(f"HP {hero.name} sekarang {hero.hp}")

# class utama pembungkus alur program
class Game:
    def __init__(self):
        # nampung array hero dan item
        self.heroes = []
        self.items = {}

    def main(self):
        # loop masukin data hero
        jumlah_hero = int(input("Masukkan jumlah hero: "))
        for i in range(jumlah_hero):
            data_hero = input(f"Hero {i+1} (format: Nama%Attack): ")
            parts = data_hero.split("%")
            # buat objek hero trus masukin list
            hero_baru = Hero(parts[0], int(parts[1]))
            self.heroes.append(hero_baru)

        # loop masukin data item
        jumlah_item = int(input("Masukkan jumlah item: "))
        for i in range(jumlah_item):
            data_item = input(f"Item {i+1} (format: Nama;Damage): ")
            parts = data_item.split(";")
            # jadikan dict dengan key nama item
            item_baru = Item(parts[0], int(parts[1]))
            self.items[parts[0]] = item_baru

        # loop milih dan pasang senjata
        print("=== PASANG SENJATA ===")
        while True:
            command = input("Command (PASANG;Hero;Item / DONE): ")
            if command == "DONE":
                break
                
            parts = command.split(";")
            if parts[0] == "PASANG":
                nama_h = parts[1]
                nama_i = parts[2]
                
                # cari hero dan bind itemnya
                for hero in self.heroes:
                    if hero.name == nama_h:
                        if nama_i in self.items:
                            hero.set_item(self.items[nama_i])
                        print(f"{nama_h} berhasil memakai {nama_i} !")
                        break

        # mulai battle level 1
        print("=== LEVEL 1 ===")
        data_enemy = input("Enemy Level 1 (format: Nama*HP): ")
        parts = data_enemy.split("*")
        enemy_1 = BasicEnemy(parts[0], int(parts[1]))
        self.battle(enemy_1)

        print()

        # lanjut battle level 2
        print("=== LEVEL 2 ===")
        data_enemy = input("Enemy Level 2 (format: Nama*HP): ")
        parts = data_enemy.split("*")
        enemy_2 = ShieldEnemy(parts[0], int(parts[1]))
        self.battle(enemy_2)

        print()

        # babak akhir lawan bos
        print("=== LEVEL 3 ===")
        data_enemy = input("Enemy Level 3 (format: Nama*HP): ")
        parts = data_enemy.split("*")
        enemy_3 = BossEnemy(parts[0], int(parts[1]))
        self.battle(enemy_3)

    # logika turn masing-masing hero
    def battle(self, enemy):
        print("=== MULAI MENYERANG ===")
        for hero in self.heroes:
            # stop kalo musuh udh keburu kalah
            if enemy.hp <= 0:
                break
            
            # trigger hero untuk attack musuh
            hero.attack(enemy)
            
            # cek sisa hp musuh paska dipukul
            if enemy.hp == 0:
                print(f"{enemy.name} berhasil dikalahkan!")
                break
                
        # info sisa hp akhir kalo blm beres
        if enemy.hp > 0:
            print(f"{enemy.name} masih hidup dengan HP {enemy.hp}")

# dijalanin dari sini
if __name__ == "__main__":
    game = Game()
    game.main()
