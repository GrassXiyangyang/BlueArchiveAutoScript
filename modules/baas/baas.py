from common import config


def load_data(self, ui):
    try:
        ui.save.clicked.disconnect()
    except RuntimeError:
        pass
    ui.save.clicked.connect(self.call_save_config)
    ui.serial.setText(self.bc['baas']['serial'])
    ui.pkg.setText(self.bc['baas']['package'])
    ui.ss_rate.setText(str(self.bc['baas']['ss_rate']))


def save_config(self, ui):
    config.load_ba_config(self)
    self.bc['baas']['serial'] = ui.serial.text()
    self.bc['baas']['ss_rate'] = float(ui.ss_rate.text())
    self.bc['baas']['package'] = ui.pkg.text()
    config.save_ba_config(self)
