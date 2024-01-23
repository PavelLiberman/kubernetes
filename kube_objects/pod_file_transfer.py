import os
import sys
import tarfile
import tempfile


class PodFileTransferMixin:
    def copy_file_to_pod(self, source_file_path: str, destination_path: str):
        """
        Copies a file from the local filesystem to a specified path in a pod.

        This method calculates the size of the file, creates a TAR archive, and streams it
        to the specified pod.

        Parameters:
        source_file_path (str): Path of the source file on the local filesystem.
        destination_path (str): Path inside the pod.
        """
        exec_command = ['tar', 'xvf', '-', '-C', destination_path]
        resp = self.get_namespaced_pod_exec_stream(exec_command)
        try:
            with tempfile.TemporaryFile() as tar_buffer:
                self._create_tar_buffer(tar_buffer, source_file_path)
                print(f"Uploading {os.path.basename(source_file_path)}.")
                self._stream_to_pod(tar_buffer, resp)
        except Exception as e:
            print(f'Exception when copying file to the pod: {e}\n')

    def copy_file_from_pod(self, source_file_path: str, destination_path: str):
        """
        Copies a file from a pod to the local host.

        Parameters:
        source_file_path (str): Path of the file inside the pod.
        destination_path (str): Local filesystem destination path.
        """
        base_dir, file_name = os.path.split(source_file_path)
        exec_command = ['tar', 'cmf', '-', '-C', base_dir, file_name]
        resp = self.get_namespaced_pod_exec_stream(exec_command)
        with tempfile.NamedTemporaryFile() as tar_buffer:
            print(f"Downloading {os.path.basename(source_file_path)}")
            self._stream_from_pod(resp, tar_buffer)
            self._extract_tar_to_destination(tar_buffer, destination_path)

    def _create_tar_buffer(self, tar_buffer, source_file_path):
        """
        Creates a TAR buffer for a given file.

        Parameters:
        tar_buffer (TemporaryFile): A temporary file object used for creating the TAR archive.
        source_file_path (str): Path of the file to be added to the TAR archive.
        """
        with tarfile.open(fileobj=tar_buffer, mode='w') as tar:
            tar.add(source_file_path, arcname=os.path.basename(source_file_path))
        tar_buffer.seek(0)

    def _stream_to_pod(self, tar_buffer, resp):
        """
        Streams a TAR buffer to a pod.

        Parameters:
        tar_buffer (TemporaryFile): The TAR buffer to be streamed.
        resp (Stream): Stream object for communicating with the pod.
        file_size_in_gb (float): Size of the file being streamed, in gigabytes.
        """
        total_bytes_written = 0
        while resp.is_open():
            chunk = tar_buffer.read(1024)
            if chunk:
                resp.write_stdin(chunk)
                total_bytes_written += len(chunk)
                uploaded = total_bytes_written
                print(f"Uploading: {uploaded} bytes ...", end='\r')
            else:
                break
        resp.close()
        print("\nUpload complete.")

    def _stream_from_pod(self, resp, tar_buffer):
        """
        Streams data from a pod into a TAR buffer.

        Parameters:
        resp (Stream): Stream object for receiving data from the pod.
        tar_buffer (NamedTemporaryFile): Temporary file to store the TAR archive.
        """
        total_bytes_read = 0
        while resp.is_open():
            resp.update(timeout=1)
            if resp.peek_stdout():
                stdout = resp.read_stdout()
                total_bytes_read += len(stdout)
                tar_buffer.write(stdout.encode())
                print(f"Downloaded {total_bytes_read} bytes ...", end='\r')
            if resp.peek_stderr():
                print("Error:", resp.read_stderr(), file=sys.stderr)
        resp.close()
        print("\nDownload complete.")

    def _extract_tar_to_destination(self, tar_buffer, destination_path):
        """
        Extracts a TAR buffer to a specified destination.

        Parameters:
        tar_buffer (NamedTemporaryFile): The TAR buffer to be extracted.
        destination_path (str): Path where the contents of the TAR buffer should be extracted to.
        """
        tar_buffer.seek(0)
        with tarfile.open(fileobj=tar_buffer, mode='r') as tar:
            tar.extractall(destination_path)
