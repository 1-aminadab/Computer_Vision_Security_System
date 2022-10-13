import smtplib
import imghdr
from datetime import datetime
from email.message import EmailMessage
#### *Face recognition *###
import cv2
### * send sms import * ###
from twilio.rest import Client
import keys
#############################
import psutil
from qt_material import *
from ui_interface import *
################### *                * ###########################
###############################################
#GLOBAL
platforms = {
    'linux': 'Linux',
    'linux1': 'Linux',
    'linux2': 'Linux',
    'darwin': 'OS X',
    'win32': 'Windows',
}
from multiprocessing import cpu_count
import time
import datetime
import platform


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        ################# * Load the style sheet * ##################
        apply_stylesheet(app, theme='dark_cyan.xml')

        self.setWindowIcon(QtGui.QIcon('AASTU_logo.png'))
        self.setWindowTitle("System Monitor");
        #######################################


        # ###### apply shadow to central widget #####
        # self.ui.centralwidget.setGraphicsEffect(self.shadow)
        self.ui.pushButton_4.setText("");
        self.ui.label_8.setStyleSheet('margin-left:-20px; font-size:18px; color:black')
        self.ui.label_3.setStyleSheet('font-size:23px; color:#0c0026')
        self.ui.scrollArea.setStyleSheet('color:#222')
        ######## set window title #######


        ######################################################
        # minimize, close and restore buttons
        #####################################################

        # Minimize_window
        self.ui.minimize_button.clicked.connect(lambda: self.showMinimized())
        # close window
        self.ui.close_button.clicked.connect(lambda: self.close())
        #restore/maximise window
        self.ui.restore_button.clicked.connect(lambda: self.restore_or_maximize_window())

        ###########################################
        # Stacked page navigation using side menu bar
        ##########################################

        # navigation to CPU page
        self.ui.cpu_page_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.cpu_and_storage))
        # navigation to Battery page
        self.ui.battery_page_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.battery))
        # navigation to System info page
        self.ui.system_inf_page_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.system_info))
        # navigation to Activity page
        self.ui.activity_page_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.activity))
        # navigation to Storage page
        self.ui.storage_page_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.storage))
        # navigation to Sensor page
        self.ui.sensor_page_btn.clicked.connect(self.securityCam)
        # navigation to Network page
        self.ui.network_page_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.network))

        ##############################
        ############################3

        self.show()
        self.battery()
        self.cpu_ram()
        self.system_info()
        self.processes()
        # self.storage()
        self.sensor()
        self.network()

    def securityCam(self):
        cascPath = os.path.dirname(cv2.__file__) + "/data/haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(cascPath)
        ####################################################################
        video_capture = cv2.VideoCapture(0)
        img_counter = 0
        rate_counter = 0

        ###################### * FUNCTION TO SEND EMAIL * ####################
        ######################################################################
        def SendEmail(attachment_image):
            Email_Address = '4ethiochild@gmail.com';
            Email_Password = 'vkzhvrbokguntdfr'

            msg = EmailMessage()
            msg['Subject'] = 'Team Security System';
            msg['From'] = Email_Address;
            msg['To'] = Email_Address;
            msg.set_content(
                'Some one is waving around me do i need to take action')

            with open(attachment_image, 'rb') as f:
                file_data = f.read()
                file_type = imghdr.what(f.name)
                file_name = f.name

            msg.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name)
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(Email_Address, Email_Password);

                smtp.send_message(msg)

        ################################## * FUNCTION TO SEND SMS * ##################
        ##############################################################################
        def Send_SMS():
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")

            client = Client(keys.account_sid, keys.auth_token)

            message = client.messages.create(
                body=f"some one is waving at me \n {current_time}",
                from_=keys.twilio_phone_number,
                to=keys.my_phone_number
            )
            print(message)


        while True:
            # Capture frame-by-frame
            ret, frames = video_capture.read()
            gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)

            if not ret:
                print("failed to grab frame")
                break
            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 50),
                flags=cv2.CASCADE_SCALE_IMAGE

            )

            # Draw a rectangle around the faces
            for (x, y, w, h) in faces:
                cv2.rectangle(frames, (x, y), (x + w, y + h), (255, 255,0 ), 2)

                if (rate_counter % 40) == 0:
                    img_name = "opencv_frame_{}.png".format(img_counter)
                    cv2.imwrite(img_name,frames)
                    img_counter += 1
                    ############################
                    SendEmail(img_name)
                    #######################
                    # Send_SMS()
                    ##########################
                    print(img_name)
                rate_counter += 1

            cv2.imshow('Security Camera', frames)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        video_capture.release()
        cv2.destroyAllWindows()


       ############################
        #Get cpu and ram information
       ############################
    def cpu_ram(self):
        self.ui.ram_info_frame.setStyleSheet('font-size:15px;background-color:#4a8f8a')
        self.ui.cpu_info_frame.setStyleSheet('font-size:15px;background-color:#7402ff')
        self.ui.label_11.setStyleSheet('font-size:20px; color:#2b0244; border-bottom:2px solid #413aaa')
        self.ui.label_12.setStyleSheet('font-size:20px; color:#2b0244; border-bottom:2px solid #413aaa')
        self.ui.label_13.setStyleSheet('font-size:20px; color:#2b0244; border-bottom:2px solid #413aaa ')

        self.ui.label_17.setStyleSheet('font-size:20px; color:#2b0244; border-bottom:2px solid #008a67 ')
        self.ui.label_19.setStyleSheet('font-size:20px; color:#2b0244; border-bottom:2px solid #008a67')
        self.ui.label_21.setStyleSheet('font-size:20px; color:#2b0244; border-bottom:2px solid #008a67 ')
        self.ui.label_23.setStyleSheet('font-size:20px; color:#2b0244; border-bottom:2px solid #008a67 ')
        self.ui.label_25.setStyleSheet('font-size:20px; color:#2b0244; border-bottom:2px solid #008a67 ')

        ###############################################################
        totalRam = 1.0
        totalRam = psutil.virtual_memory()[0] * totalRam
        totalRam = totalRam/(1024 * 1024 * 1024)
        self.ui.total_ram.setText(str("{:.4f}".format(totalRam) + 'GB'))

        ###############################################################

        self.ui.cpu_count.setStyleSheet('background-color: #413aaa; border:2px solid #413aaa')
        self.ui.cpu_per.setStyleSheet('background-color: #413aaa; border:2px solid #413aaa')
        self.ui.cpu_main_core.setStyleSheet('background-color: #413aaa;border:2px solid #413aaa')

        self.ui.total_ram.setStyleSheet('background-color: #008a67; border:2px solid #008f67')
        self.ui.used_ram.setStyleSheet('background-color: #008a67; border:2px solid #008f67')
        self.ui.ram_usage.setStyleSheet('background-color: #008a67;border:2px solid #008f67')
        self.ui.available_ram.setStyleSheet('background-color: #008a67;border:2px solid #008f67')
        self.ui.free_ram.setStyleSheet('background-color: #008a67;border:2px solid #008f67')

        ##############################################################
        availRam = 1.0
        availRam = psutil.virtual_memory()[1] * availRam
        availRam = availRam / (1024 * 1024 * 1024)
        self.ui.available_ram.setText(str("{:.4f}".format(availRam) + 'GB'))
      
        ramUsed = 1.0
        ramUsed  = psutil.virtual_memory()[3] * ramUsed
        ramUsed  = ramUsed / (1024 * 1024 * 1024)
        self.ui.used_ram.setText(str("{:.4f}".format(ramUsed ) + 'GB'))

        ramFree = 1.0
        ramFree = psutil.virtual_memory()[4] * ramFree
        ramFree = ramFree / (1024 * 1024 * 1024)
        self.ui.free_ram.setText(str("{:.4f}".format(ramFree) + 'GB'))

        core = cpu_count()
        self.ui.cpu_count.setText(str(core))

        ramUsage = 1.0
        ramUsage = psutil.virtual_memory()[2] * ramUsage
        ramUsage = ramUsage / (1024 * 1024 * 1024)
        self.ui.ram_usage.setText(str("{:.4f}".format(ramUsage) + 'GB'))
        # ramUsage = str(psutil.virtual_memory()[2]) +'%'
        # self.ui.ram_usage.setText(str("{:.4f}".format(totalRam) + 'GB'))

        cpuPer = psutil.cpu_percent()
        self.ui.cpu_per.setText(str(cpuPer) + "%")

        cpuMainCore = psutil.cpu_count(logical=False)
        self.ui.cpu_main_core.setText(str(cpuMainCore))

         ########################
        #function to convert second to hour
        #################################
    def secs2hours(self,secs):
        mm, ss = divmod(secs, 60)
        hh, mm = divmod(mm, 60)
        return "%d:%02d:%02d (H:M:S)" %(hh, mm, ss)
        self.ui.system_time.setText(str(date))
       ###################################3
       #Get system battery information
    def battery(self):
        batt = psutil.sensors_battery()
        ########### EDIT THE WIDTH ############
        self.ui.battery_status.setFixedWidth(300)
        self.ui.battery_charge.setFixedWidth(300)
        self.ui.battery_time_left.setFixedWidth(300)
        self.ui.battery_plugged.setFixedWidth(300)

        self.ui.battery_status.setFixedHeight(22)
        self.ui.battery_charge.setFixedHeight(22)
        self.ui.battery_time_left.setFixedHeight(22)
        self.ui.battery_plugged.setFixedHeight(22)
        self.ui.frame.setStyleSheet('margin-bottom:120px')

        self.ui.battery_status.setStyleSheet('background-color: #413aaa; border:2px solid #413aaa; ')
        self.ui.battery_charge.setStyleSheet('background-color: #413aaa; border:2px solid #413aaa')
        self.ui.battery_time_left.setStyleSheet('background-color: #413aaa; border:2px solid #413aaa; ')
        self.ui.battery_plugged.setStyleSheet('background-color: #413aaa; border:2px solid #413aaa')


        self.ui.label_28.setStyleSheet('font-size:20px; color:#2b0244; border-bottom:2px solid #413aaa;')
        self.ui.label_29.setStyleSheet('font-size:20px; color:#2b0244;  border-bottom:2px solid #413aaa;')
        self.ui.label_30.setStyleSheet('font-size:20px; color:#2b0244; border-bottom:2px solid #413aaa;')
        self.ui.label_31.setStyleSheet('font-size:20px; color:#2b0244; border-bottom:2px solid #413aaa; ')

        self.ui.label_28.setFixedWidth(300)
        self.ui.label_29.setFixedWidth(300)
        self.ui.label_30.setFixedWidth(300)
        self.ui.label_30.setFixedHeight(55)
        self.ui.label_30.setStyleSheet('margin-top:12px; border-size:2px; border-color:red')
        self.ui.label_31.setFixedWidth(300)
        self.ui.label_27.setStyleSheet('font-size:25px; background-color:#5f01a2;')
        self.ui.frame.setStyleSheet('font-size:15px;background-color:#4a8f8a; ')




        ########################################
        if not hasattr(psutil, "sensor_battery"):
            self.ui.battery_status.setText("Platform not supported")
        if batt is None:
            self.ui.battery_status.setText("No battery installed")
        if batt.power_plugged:
            self.ui.battery_charge.setText(str(round(batt.percent, 2)) + "%")
            self.ui.battery_time_left.setText("N/A")
            if batt.percent < 100:
                self.ui.battery_status.setText("Charging")
            else:
                self.ui.battery_status.setText("Fully Charged")
            self.ui.battery_plugged.setText("Yes")
        else:
            self.ui.battery_charge.setText(str(round(batt.percent, 2)) + "%")
            self.ui.battery_time_left.setText((self.secs2hours(batt.secsleft)))

            if batt.percent < 100:
                self.ui.battery_status.setText("DisCharging")
            else:
                self.ui.battery_status.setText("Fully Charged")
            self.ui.battery_plugged.setText("No")

     #################################################
    #  Get system information
    ################################################
    def system_info(self):
        ################## style the lables ##################################

        self.ui.system_machine.setStyleSheet('padding-bottom:10px; border :1.7px solid #abc501; padding-top:8px')
        self.ui.system_processor.setStyleSheet('padding-bottom:10px; border :1.7px solid #00ac56; padding-top:8px')
        self.ui.system_time.setStyleSheet('padding-bottom:10px; border :1.7px solid #b4003f; padding-top:8px')
        self.ui.system_platform.setStyleSheet('padding-bottom:10px; border:1.7px solid #00ac56; padding-top:8px')
        self.ui.system_version.setStyleSheet('padding-bottom:10px; border:1.7px solid #abc501; padding-top:8px')
        self.ui.system_system.setStyleSheet('padding-bottom:10px; border:1.7px solid #b4003f; padding-top:8px')



        time = datetime.datetime.now().strftime("%I:%M:%S %p")
        self.ui.system_date.setText(str(time))
        date = datetime.datetime.now().strftime("%y-%m-%d")
        self.ui.system_time.setText(str(date))

        self.ui.system_machine.setText(platform.machine())
        self.ui.system_version.setText(platform.version())
        self.ui.system_platform.setText(platform.platform())
        self.ui.system_system.setText(platform.system())
        self.ui.system_processor.setText(platform.processor())

    ######################################################
    # A Function that create table widget
    ######################################################
    def create_table_widget(self, rowPosition, columnPosition, text, tableName):
        qtablewidgetitem = QTableWidgetItem()
        getattr(self.ui, tableName).setItem(rowPosition, columnPosition, qtablewidgetitem)
        qtablewidgetitem = getattr(self.ui, tableName).item(rowPosition, columnPosition)
        qtablewidgetitem.setText(text)



 ######################################################
 # RUNNING PROCESSES
 ######################################################

    def processes(self):
        for x in psutil.pids():
            rowPosition = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(rowPosition)

            try:
                process = psutil.Process(x)
                self.create_table_widget(rowPosition, 0, str(process.pid), "tableWidget")
                self.create_table_widget(rowPosition, 1, process.name(), "tableWidget")
                self.create_table_widget(rowPosition, 2, process.status(), "tableWidget")
                self.create_table_widget(rowPosition, 3, str(datetime.datetime.utcfromtimestamp(process.create_time()).strftime('%y-%m-%d %H:%M:%S')), "tableWidget")




            except Exception as e:
                print(e)
            self.ui.activity_search.textChanged.connect(self.findName)
            self.ui.activity_search.setStyleSheet('color:black; font-size:15px; background-color:#555')

    def findName(self):
        name = self.ui.activity_search.text().lower()
        for row in range(self.ui.tableWidget.rowCount()):
            item = self.ui.tableWidget.item(row, 1)
            self.ui.tableWidget.setRowHidden(row, name not in item.text().lower())

    ######################################################
     # STORAGE PARTITION
     ######################################################

    def storage(self):
        global platforms
        storage_device = psutil.disk_partitions(all=False)
        z=0
        for x in storage_device:
            rowPosition = self.ui.storageTable.rowCount();
            self.ui.storageTable.insertRow((rowPosition))

            self.create_table_widget(rowPosition, 0, x.device, "storageTable")
            self.create_table_widget(rowPosition, 1, x.mountpoint, "storageTable")
            self.create_table_widget(rowPosition, 2, x.fstype, "storageTable")
            self.create_table_widget(rowPosition, 3, x.opts, "storageTable")

            if sys.platform == 'linux' or sys.platform == 'linux1' or sys.platform == 'linux2':
                self.create_table_widget(rowPosition, 4, str(x.maxfile), "storageTable")
                self.create_table_widget(rowPosition, 5, str(x.maxpath), "storageTable")
            else:
                self.create_table_widget(rowPosition, 4, "Function not available" + platforms[sys.platform],"storageTable")
                self.create_table_widget(rowPosition, 5, "Function not available" + platforms[sys.platform],"storageTable")
            ## print(disk_usage(x.device)
            disk_usage = shutil.disk_usage(x.mountpoint)

            ## print(disk_usage.tool)

            self.create_table_widget(rowPosition, 6, str((disk_usage.total/(1024 * 1024 * 1024))) + "GB", "storageTable")
            self.create_table_widget(rowPosition, 7, str((disk_usage.free / (1024 * 1024 * 1024))) + "GB",
                                     "storageTable")
            self.create_table_widget(rowPosition, 8, str((disk_usage.used / (1024 * 1024 * 1024))) + "GB",
                                     "storageTable")

        ######################################################
        # Sensor Information
        ######################################################
    def sensor(self):
        if sys.platform == 'linux' or sys.platform == 'linux' or sys.platform == 'linux2':
            for x in psutil.sensors_temperatures():
                for y in psutil.sensors_temperatures()[x]:
                    rowPosition = self.ui.sensorTable.rowCount()
                    self.ui.sensorTable.insertRow(rowPosition)

                    self.create_table_widget(rowPosition, 0, x, "sensorTable")
                    self.create_table_widget(rowPosition, 1, y.label, "sensorTable")
                    self.create_table_widget(rowPosition, 2, str(y.current), "sensorTable")
                    self.create_table_widget(rowPosition, 3, str(y.high), "sensorTable")
        else:
            global platforms

            rowPosition = self.ui.sensorTable.rowCount()
            self.ui.sensorTable.insertRow(rowPosition)
            self.create_table_widget(rowPosition, 0, "Function not supported on " + platforms[sys.platform],"sensorTable")
            self.create_table_widget(rowPosition, 0, "N/A", "sensorTable")
            self.create_table_widget(rowPosition, 1, "N/A", "sensorTable")
            self.create_table_widget(rowPosition, 2, "N/A", "sensorTable")
            self.create_table_widget(rowPosition, 3, "N/A", "sensorTable")

     #####################################
    # NETWORK fUNCTION
    #####################################
    def network(self):
        self.ui.scrollArea.setStyleSheet('font-size:15px')
        #Net stats
        for x in psutil.net_if_stats():
            z = psutil.net_if_stats()
            #Create new row
            rowPosition = self.ui.net_stats_table.rowCount()
            self.ui.net_stats_table.insertRow(rowPosition)
            self.ui.net_stats_table.setStyleSheet('background-color:green; color:black; font-size:15px;min-width:20px')

            self.create_table_widget(rowPosition, 0, x, "net_stats_table")
            self.create_table_widget(rowPosition, 1, str(z[x].isup), "net_stats_table")
            self.create_table_widget(rowPosition, 2, str(z[x].duplex), "net_stats_table")
            self.create_table_widget(rowPosition, 3, str(z[x].speed), "net_stats_table")
            self.create_table_widget(rowPosition, 4, str(z[x].mtu), "net_stats_table")


         ###network i/o
        for x in psutil.net_io_counters(pernic=True):
            z = psutil.net_io_counters(pernic=True)
            # Create new row
            rowPosition = self.ui.net_io_table.rowCount()
            self.ui.net_io_table.insertRow(rowPosition)
            self.ui.net_io_table.setStyleSheet('background-color:#8d8d2b; color:black; font-size:15px; min-width:20px')

            self.create_table_widget(rowPosition, 0, x, "net_io_table")
            self.create_table_widget(rowPosition, 1, str(z[x].bytes_sent), "net_io_table")
            self.create_table_widget(rowPosition, 2, str(z[x].bytes_recv), "net_io_table")
            self.create_table_widget(rowPosition, 3, str(z[x].packets_sent), "net_io_table")
            self.create_table_widget(rowPosition, 4, str(z[x].packets_recv), "net_io_table")
            self.create_table_widget(rowPosition, 1, str(z[x].errin), "net_io_table")
            self.create_table_widget(rowPosition, 2, str(z[x].errout), "net_io_table")
            self.create_table_widget(rowPosition, 3, str(z[x].dropin), "net_io_table")
            self.create_table_widget(rowPosition, 4, str(z[x].dropout), "net_io_table")

        ##### Network address
            z = psutil.net_if_addrs()
            for y in z[x]:
                # Create new row
                rowPosition = self.ui.net_address_table.rowCount()
                self.ui.net_address_table.insertRow(rowPosition)
                self.ui.net_address_table.setStyleSheet('background-color:red; color:black; font-size:15px; min-width:20px')

                self.create_table_widget(rowPosition, 0, str(x), "net_address_table")
                self.create_table_widget(rowPosition, 1, str(y.family), "net_address_table")
                self.create_table_widget(rowPosition, 2, str(y.address), "net_address_table")
                self.create_table_widget(rowPosition, 3, str(y.netmask), "net_address_table")
                self.create_table_widget(rowPosition, 4, str(y.broadcast), "net_address_table")
                self.create_table_widget(rowPosition, 5, str(y.ptp), "net_address_table")


            #network connection
        for x in psutil.net_connections():
            z = psutil.net_connections()
            # Create new row
            rowPosition = self.ui.net_connections_table.rowCount()
            self.ui.net_connections_table.insertRow(rowPosition)
            self.ui.net_connections_table.setStyleSheet('background-color:blue; color:black; font-size:15px; min-width:20px')

            self.create_table_widget(rowPosition, 0, str(x.fd), "net_connections_table")
            self.create_table_widget(rowPosition, 1, str(x.family), "net_connections_table")
            self.create_table_widget(rowPosition, 2, str(x.type), "net_connections_table")
            self.create_table_widget(rowPosition, 3, str(x.laddr), "net_connections_table")
            self.create_table_widget(rowPosition, 4, str(x.raddr), "net_connections_table")
            self.create_table_widget(rowPosition, 5, str(x.status), "net_connections_table")
            self.create_table_widget(rowPosition, 6, str(x.pid), "net_connections_table")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())