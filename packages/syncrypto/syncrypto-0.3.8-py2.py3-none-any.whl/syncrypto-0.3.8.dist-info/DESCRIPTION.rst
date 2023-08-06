Synchronize a folder with its encrypted content

Home-page: https://github.com/liangqing/syncrypto
Author: Qing Liang
Author-email: liangqing226@gmail.com
License: http://www.apache.org/licenses/LICENSE-2.0
Description: Synchronize a folder with its encrypted content
        ===============================================
        
        .. image:: https://img.shields.io/pypi/v/syncrypto.svg
            :target: https://pypi.python.org/pypi/syncrypto/
            :alt: Latest Version
        
        .. image:: https://travis-ci.org/liangqing/syncrypto.svg?branch=master
            :target: https://travis-ci.org/liangqing/syncrypto
            :alt: Build And Test Status
        
        .. image:: https://codecov.io/github/liangqing/syncrypto/coverage.svg?branch=master
            :target: https://codecov.io/github/liangqing/syncrypto?branch=master
            :alt: Code Coverage
        
        .. image:: https://landscape.io/github/liangqing/syncrypto/master/landscape.svg?style=flat
           :target: https://landscape.io/github/liangqing/syncrypto/master
           :alt: Code Health
        
        Introduction
        ============
        You can use ``syncrypto`` to encrypt a folder to another folder which contains the
        corresponding encrypted content.
        
        The most common scenario is\:
        
        .. code-block:: text
        
                                 syncrypto                         syncrypto
          plaintext folder A  <-------------> encrypted folder B <-----------> plaintext folder C
            in machine X                       in cloud storage                 in machine Y
        
        The files in encrypted folder B are encrypted, so you can store it in any unsafe
        environment, such as cloud service(Dropbox/OneDrive), USB storage or any other
        storage that you can not control.
        
        Each plaintext file has a corresponding encrypted file in the encrypted folder,
        so if you modify one file in plaintext folder, there will be only one file
        modified in the encrypted folder after synchronization. This make sure the
        synchronization only changes the necessary content in encrypted folder, and is
        very useful for file based cloud storage service to synchronizing minimal contents.
        
        The synchronization is two-way, files not only syncing from plain text folder to
        encrypted folder, but also syncing from encrypted folder to plain text folder.
        ``syncrypto`` will choose the newest file.
        
        If conflict happens, ``syncrypto`` will rename the plaintext file(add 'conflict'
        word in it), and sync the encrypted file.
        
        ``syncrypto`` never delete files, if files or folders should be deleted or over
        written by the syncing algorithm, ``syncrypto`` just move the files or folders
        to the trash, the trash in encrypted folder located at _syncrypto/trash,
        at .syncrypto/trash in plaintext folder. Files in encrypted folder's trash are
        also encrypted. You can delete any files in trash in any time if you make sure
        the files in it are useless.
        
        
        Installation
        ============
        
        Support Platform
        ----------------
        
        ``syncrypto`` supports both python 2 and python 3, and is tested_ in\:
        
        .. _tested: https://travis-ci.org/liangqing/syncrypto
        
        * python 2.6
        * python 2.7
        * python 3.3
        * python 3.4
        
        And support Linux, OS X, Windows operating systems
        
        Install Dependencies
        --------------------
        
        **If you are using windows, just jump to next**
        
        Because ``syncrypto`` rely on cryptography_ , so need to install some
        dependencies before install ``syncrypto``\:
        
        .. _cryptography: https://github.com/pyca/cryptography
        
        For Debian and Ubuntu, the following command will ensure that the required
        dependencies are installed\:
        
        .. code-block:: bash
        
            sudo apt-get install build-essential libssl-dev libffi-dev python-dev
        
        
        For Fedora and RHEL-derivatives, the following command will ensure that the
        required dependencies are installed\:
        
        .. code-block:: bash
        
            sudo yum install gcc libffi-devel python-devel openssl-devel
        
        For OS X, run\:
        
        .. code-block:: bash
        
            xcode-select --install
        
        
        Install By pip
        --------------
        
        After installing all dependencies, you can install ``syncrypto`` by pip_ \:
        
        .. _pip: https://pip.pypa.io/en/latest/installing.html
        
        .. code-block:: bash
        
            pip install syncrypto
        
        
        Usage
        =====
        
        Synchronization
        ---------------
        
        .. code-block:: bash
        
            syncrypto [encrypted folder] [plaintext folder]
        
        It will prompt you to input a password, if the encrypted folder is empty,
        the input password will be set to the encrypted folder, or it will be used
        to verify the password you set before (take it easy, ``syncrypto`` never store
        plaintext password)
        
        If you don't want input password in interactive mode, you can use --password-file
        option\:
        
        .. code-block:: bash
        
            syncrypto [encrypted folder] [plaintext folder] --password-file [password file path]
        
        The password file contains the password in it.
        
        Notice that the first argument is encrypted folder, and the second one is
        plaintext folder.
        
        
        
Platform: UNKNOWN
Classifier: License :: OSI Approved :: Apache Software License
Classifier: Programming Language :: Python :: 2
Classifier: Programming Language :: Python :: 2.6
Classifier: Programming Language :: Python :: 2.7
Classifier: Programming Language :: Python :: 3
Classifier: Programming Language :: Python :: 3.3
Classifier: Programming Language :: Python :: 3.4
Classifier: Topic :: Communications :: File Sharing
