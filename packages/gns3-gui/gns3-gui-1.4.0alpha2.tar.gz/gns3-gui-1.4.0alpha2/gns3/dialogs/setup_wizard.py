# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 GNS3 Technologies Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import os

from gns3.qt import QtCore, QtWidgets
from gns3.servers import Servers
from ..gns3_vm import GNS3VM
from ..dialogs.preferences_dialog import PreferencesDialog
from ..ui.setup_wizard_ui import Ui_SetupWizard
from ..utils.progress_dialog import ProgressDialog
from ..utils.wait_for_vm_worker import WaitForVMWorker


class SetupWizard(QtWidgets.QWizard, Ui_SetupWizard):

    """
    Base class for VM wizard.
    """

    def __init__(self, parent):

        super().__init__(parent)
        self.setupUi(self)

        self.setWizardStyle(QtWidgets.QWizard.ModernStyle)
        if sys.platform.startswith("darwin"):
            # we want to see the cancel button on OSX
            self.setOptions(QtWidgets.QWizard.NoDefaultButton)

        self._server = Servers.instance().localServer()
        self.uiRefreshPushButton.clicked.connect(self._refreshVMListSlot)
        self.uiVmwareRadioButton.clicked.connect(self._listVMwareVMsSlot)
        self.uiVirtualBoxRadioButton.clicked.connect(self._listVirtualBoxVMsSlot)
        settings = parent.settings()
        self.uiShowCheckBox.setChecked(settings["hide_setup_wizard"])

        # by default all radio buttons are unchecked
        self.uiVmwareRadioButton.setAutoExclusive(False)
        self.uiVirtualBoxRadioButton.setAutoExclusive(False)
        self.uiVmwareRadioButton.setChecked(False)
        self.uiVirtualBoxRadioButton.setChecked(False)

    def _listVMwareVMsSlot(self):
        """
        Slot to refresh the VMware VMs list.
        """

        self.uiVirtualBoxRadioButton.setChecked(False)
        from gns3.modules import VMware
        settings = VMware.instance().settings()
        if not os.path.exists(settings["vmrun_path"]):
            QtWidgets.QMessageBox.critical(self, "VMware", "VMware vmrun tool could not be found, VMware or the VIX API is probably not installed")
            return
        self._refreshVMListSlot()

    def _listVirtualBoxVMsSlot(self):
        """
        Slot to refresh the VirtualBox VMs list.
        """

        self.uiVmwareRadioButton.setChecked(False)
        from gns3.modules import VirtualBox
        settings = VirtualBox.instance().settings()
        if not os.path.exists(settings["vboxmanage_path"]):
            QtWidgets.QMessageBox.critical(self, "VirtualBox", "VBoxManage could not be found, VirtualBox is probably not installed")
            return
        self._refreshVMListSlot()

    def showit(self):
        """
        Either this dialog should be automatically showed at startup.

        :returns: boolean
        """

        return not self.uiShowCheckBox.isChecked()

    def _setPreferencesPane(self, dialog, name):
        """
        Finds the first child of the QTreeWidgetItem name.

        :param dialog: PreferencesDialog instance
        :param name: QTreeWidgetItem name

        :returns: current QWidget
        """

        pane = dialog.uiTreeWidget.findItems(name, QtCore.Qt.MatchFixedString)[0]
        child_pane = pane.child(0)
        dialog.uiTreeWidget.setCurrentItem(child_pane)
        return dialog.uiStackedWidget.currentWidget()

    def validateCurrentPage(self):
        """
        Validates the settings.
        """

        gns3_vm = GNS3VM.instance()
        servers = Servers.instance()
        if self.currentPage() == self.uiVMWizardPage:
            vmname = self.uiVMListComboBox.currentText()
            if vmname:
                # save the GNS3 VM settings
                vm_settings = {"auto_start": True,
                               "vmname": vmname,
                               "vmx_path": self.uiVMListComboBox.currentData()}
                if self.uiVmwareRadioButton.isChecked():
                    vm_settings["virtualization"] = "VMware"
                elif self.uiVirtualBoxRadioButton.isChecked():
                    vm_settings["virtualization"] = "VirtualBox"
                gns3_vm.setSettings(vm_settings)
                servers.save()

                # start the GNS3 VM
                servers.initVMServer()
                worker = WaitForVMWorker()
                progress_dialog = ProgressDialog(worker, "GNS3 VM", "Starting the GNS3 VM...", "Cancel", busy=True, parent=self)
                progress_dialog.show()
                if progress_dialog.exec_():
                    gns3_vm.adjustLocalServerIP()
            else:
                return False
        elif self.currentPage() == self.uiAddVMsWizardPage:

            use_local_server = self.uiLocalRadioButton.isChecked()
            if use_local_server:
                # deactivate the GNS3 VM if using the local server
                vm_settings = {"auto_start": False}
                gns3_vm.setSettings(vm_settings)
                servers.save()
            from gns3.modules import Dynamips
            Dynamips.instance().setSettings({"use_local_server": use_local_server})
            if sys.platform.startswith("linux"):
                # IOU only works on Linux
                from gns3.modules import IOU
                IOU.instance().setSettings({"use_local_server": use_local_server})
            from gns3.modules import Qemu
            Qemu.instance().setSettings({"use_local_server": use_local_server})
            from gns3.modules import VPCS
            VPCS.instance().setSettings({"use_local_server": use_local_server})

            dialog = PreferencesDialog(self)
            if self.uiAddIOSRouterCheckBox.isChecked():
                self._setPreferencesPane(dialog, "Dynamips").uiNewIOSRouterPushButton.clicked.emit(False)
            if self.uiAddIOUDeviceCheckBox.isChecked():
                self._setPreferencesPane(dialog, "IOS on UNIX").uiNewIOUDevicePushButton.clicked.emit(False)
            if self.uiAddQemuVMcheckBox.isChecked():
                self._setPreferencesPane(dialog, "QEMU").uiNewQemuVMPushButton.clicked.emit(False)
            if self.uiAddVirtualBoxVMcheckBox.isChecked():
                self._setPreferencesPane(dialog, "VirtualBox").uiNewVirtualBoxVMPushButton.clicked.emit(False)
            if self.uiAddVMwareVMcheckBox.isChecked():
                self._setPreferencesPane(dialog, "VMware").uiNewVMwareVMPushButton.clicked.emit(False)
            dialog.exec_()
        return True

    def _refreshVMListSlot(self):
        """
        Refresh the list of VM available in VMware or VirtualBox.
        """

        if not Servers.instance().localServerIsRunning():
            QtWidgets.QMessageBox.critical(self, "Local server", "{}".format("Local server is not running"))
            return
        server = Servers.instance().localServer()
        if self.uiVmwareRadioButton.isChecked():
            server.get("/vmware/vms", self._getVMsFromServerCallback)
        elif self.uiVirtualBoxRadioButton.isChecked():
            server.get("/virtualbox/vms", self._getVMsFromServerCallback)

    def _getVMsFromServerCallback(self, result, error=False, **kwargs):
        """
        Callback for getVMsFromServer.

        :param progress_dialog: QProgressDialog instance
        :param result: server response
        :param error: indicates an error (boolean)
        """

        if error:
            QtWidgets.QMessageBox.critical(self, "VM List", "{}".format(result["message"]))
        else:
            self.uiVMListComboBox.clear()
            for vm in result:
                if self.uiVmwareRadioButton.isChecked():
                    self.uiVMListComboBox.addItem(vm["vmname"], vm["vmx_path"])
                else:
                    self.uiVMListComboBox.addItem(vm["vmname"], "")
            gns3_vm = Servers.instance().vmSettings()
            index = self.uiVMListComboBox.findText(gns3_vm["vmname"])
            if index != -1:
                self.uiVMListComboBox.setCurrentIndex(index)
            else:
                index = self.uiVMListComboBox.findText("GNS3 VM")
                if index != -1:
                    self.uiVMListComboBox.setCurrentIndex(index)
                else:
                    QtWidgets.QMessageBox.critical(self, "GNS3 VM", "Could not find a VM named 'GNS3 VM', is it imported in VMware or VirtualBox?")

    def done(self, result):
        """
        This dialog is closed.

        :param result: ignored
        """

        settings = self.parentWidget().settings()
        settings["hide_setup_wizard"] = self.uiShowCheckBox.isChecked()
        self.parentWidget().setSettings(settings)
        super().done(result)

    def nextId(self):
        """
        Wizard rules!
        """

        current_id = self.currentId()
        if self.page(current_id) == self.uiServerWizardPage and not self.uiVMRadioButton.isChecked():
            # skip the GNS3 VM page if using the local server.
            return self.uiServerWizardPage.nextId() + 1
        return QtWidgets.QWizard.nextId(self)
