import random
import PySimpleGUI as sg
import datetime

class PengaduanForm:
    # Inisialisasi GUI
    def __init__(self):
        sg.SetOptions(font=('Cambria', 10))
        sg.SetOptions(background_color='#8E7896')
        sg.SetOptions(text_element_background_color='#8E7896')
 
        column_left = [
                        [sg.Text('Nomor Laporan')],
                        [sg.Input(key='-NOMOR_LAPORAN-', size=(35, 10), readonly=True, disabled_readonly_background_color='#D3D3D3')],
                        [sg.Text('NIK Pelapor')],
                        [sg.Input(key='-NIK-', size=(35, 10))],
                        [sg.Text('Nama Lengkap')],
                        [sg.Input(key='-NAMA-', size=(35, 10))],
                        [sg.Text('Tempat Lahir')],
                        [sg.Input(key='-TEMPAT_LAHIR-', size=(35, 10))],
                        [sg.Text('Tanggal Lahir')],
                        [
                            sg.Input(key='-TANGGAL_LAHIR-', disabled=True, size=(22, 10)),
                            sg.CalendarButton('Pilih Tanggal', button_color=('#483D8B'),  target='-TANGGAL_LAHIR-', format='%d-%m-%Y')
                        ],
                        [sg.Text('Jenis Kelamin')],
                        [sg.Combo(['--Pilih Jenis Kelamin--', 'Laki-laki', 'Perempuan'], key='-JENIS_KELAMIN-', default_value='--Pilih Jenis Kelamin--', size=(33, 10), readonly=True)],
                        [sg.Text('Nomor Telepon')],
                        [sg.Input(key='-TELEPON-', size=(35, 10))],
        ]
        column_right = [
            [sg.Text('Alamat')],
            [sg.Input(key='-ALAMAT-', size=(35, 10))],
            [sg.Text('Kategori Pengaduan')],
            [sg.Combo(['Lingkungan', 'Kriminal', 'Fasilitas', 'Lainnya'], 
                      key='-KATEGORI-', 
                      default_value='--Pilih Kategori Pengaduan--', 
                      readonly=True, 
                      size=(33, 10))],
            [sg.Text('Isi Pengaduan')],
            [sg.Multiline(key='-ISI_LAPORAN-', size=(33, 12))],
            [sg.Button('Batal', button_color=('#483D8B')), 
             sg.Button('Submit', button_color=('#483D8B'))]
        ]
        self.layout = [
            [sg.Text('Form Layanan Pengaduan Masyarakat', font=('Cambria', 16), justification='center')],
            [
                sg.Column(column_left, element_justification='left', pad=((50, 50), (0, 0))),
                sg.Column(column_right, element_justification='left', pad=((50, 50), (0, 0)))],
            [
                sg.Column(
                    [
                        [sg.Text('Histori Laporan:')],
                        [sg.Table(
                            values=[],
                            headings=['Nomor Laporan', 'Tanggal', 'Kategori', 'Status'],
                            justification='left',
                            auto_size_columns=False,
                            col_widths=[13, 13, 13, 13],
                            key='-TABLE_HISTORI-',
                            enable_events=True,
                            background_color='#8E7896'
                        )],
                        [sg.Button('Hapus Histori', button_color=('#483D8B'))]

                    ],
                    element_justification='center',
                    pad=((0, 0), (40, 0)) 
                )
            ]
        ]
        self.window = sg.Window('Form Layanan Pengaduan Masyarakat', 
                                self.layout, 
                                element_justification='center', 
                                finalize=True, size=(800, 860))
        self.nomor_laporan = self.generate_nomor_laporan()
        self.histori_laporan = []
        self.window['-NOMOR_LAPORAN-'].update(self.nomor_laporan)

    # Generate nomor laporan secara acak
    def generate_nomor_laporan(self):
        nomor_laporan = str(random.randint(1000, 9999))
        return nomor_laporan

    def run(self):
        while True:
            # Membaca peristiwa yang terjadi dalam GUI
            event, values = self.window.read()
            
            # Menutup jendela GUI dan loop utama dihentikan
            if event == sg.WINDOW_CLOSED:
                break
            
            if event == 'Batal':
                self.clear_form_inputs()

            if event == '-CALENDAR-':
                selected_date = values['-CALENDAR-']
                self.window['-TANGGAL_LAHIR-'].update(selected_date)

            if event == 'Submit':
                if self.validate_input(values):
                    self.submit_pengaduan(values)
                    nomor_laporan = self.window['-NOMOR_LAPORAN-'].get()
                    sg.popup('Pengaduan berhasil disimpan.\nNomor Laporan: {}'.format(nomor_laporan), title='Berhasil')
                    self.window['-NOMOR_LAPORAN-'].update(self.generate_nomor_laporan())
                    self.clear_form_inputs()
                    self.window['-TABLE_HISTORI-'].update(values=self.histori_laporan)

            # Memeriksa apakah peristiwa berasal dari pemilihan baris pada tabel histori, jika ya,  maka indeks baris yang dipilih akan disimpan
            if event == '-TABLE_HISTORI-':
                selected_row = values['-TABLE_HISTORI-'][0]
                if selected_row != -1:
                    self.view_laporan(self.histori_laporan[selected_row])
                    
            if event == 'Hapus Histori':
                self.delete_history()
                
        self.window.close()

    # Menghapus input pada formulir dengan mengatur nilai masing-masing elemen input ke string kosong
    def clear_form_inputs(self):
        self.window['-NIK-'].update('')
        self.window['-NAMA-'].update('')
        self.window['-TEMPAT_LAHIR-'].update('')
        self.window['-TANGGAL_LAHIR-'].update('')
        self.window['-JENIS_KELAMIN-'].update('--Pilih Jenis Kelamin--')
        self.window['-TELEPON-'].update('')
        self.window['-ALAMAT-'].update('')
        self.window['-KATEGORI-'].update('--Pilih Kategori Pengaduan--')
        self.window['-ISI_LAPORAN-'].update('')
        self.window['-NOMOR_LAPORAN-'].update(self.generate_nomor_laporan())

    # Validasi input formulir untuk memastikan kolom telah diisi dengan benar
    def validate_input(self, values):
        # Memastikan kolom input tidak ada yang kosong 
        if values['-NIK-'] == '' or values['-NAMA-'] == '' or values['-TEMPAT_LAHIR-'] == '' or values['-TANGGAL_LAHIR-'] == '' or values['-JENIS_KELAMIN-'] == '--Pilih Jenis Kelamin--' or values['-TELEPON-'] == '' or values['-ALAMAT-'] == '' or values['-KATEGORI-'] == '--Pilih Kategori Pengaduan--' or values['-ISI_LAPORAN-'] == '':
            sg.popup('Mohon lengkapi semua kolom input.', title='Peringatan!')
            return False
        
        # Memeriksa apakah NIK mengandung karakter lain selain angka
        if not values['-NIK-'].isdigit():
            sg.popup('NIK hanya boleh berisi angka.', title='Peringatan!')
            return False
        
        # Memerika apakah NIK memiliki panjang tidak sama dengan 16
        if len(values['-NIK-']) != 16:
            sg.popup('NIK harus terdiri dari 16 angka.', title='Peringatan!')
            return False
        
        # Memeriksa apakah Nomor Telepon mengandung karakter lain selain angka
        if not values['-TELEPON-'].isdigit():
            sg.popup('Nomor Telepon hanya boleh berisi angka.', title='Peringatan!')
            return False
        return True

    # Menyimpan pengaduan ke dalam histori laporan
    def submit_pengaduan(self, values):
        nomor_laporan = self.window['-NOMOR_LAPORAN-'].get()
        tanggal = datetime.datetime.now().strftime('%Y-%m-%d')
        kategori = values['-KATEGORI-']
        status = 'Dalam Proses'
        self.histori_laporan.append((nomor_laporan, tanggal, kategori, status))
        self.window['-TABLE_HISTORI-'].update(values=self.histori_laporan)
     
    # Menghapus seluruh histori laporan dengan membuat menjadi sebuah daftar kosong  
    def delete_history(self):
        self.histori_laporan = []
        self.window['-TABLE_HISTORI-'].update(values=self.histori_laporan)

    # Menampilkan informasi laporan
    def view_laporan(self, laporan):
        nomor_laporan, tanggal, kategori, status = laporan
        sg.popup(f'Nomor Laporan: {nomor_laporan}\nTanggal: {tanggal}\nKategori: {kategori}\nStatus: {status}')

if __name__ == '__main__':
    form = PengaduanForm()
    form.run()