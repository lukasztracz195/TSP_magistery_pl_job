import os

from builders.PathBuilder import PathBuilder

PROFILER_IN_PROGRESS = "PROFILER_IN_PROGRESS.txt"
MEASURE_IN_PROGRESS = "MEASURE_IN_PROGRESS.txt"

path_to_profiler_file = PathBuilder().add_dir("tmp").add_file_with_extension(PROFILER_IN_PROGRESS).build()
path_to_measure_file = PathBuilder().add_dir("tmp").add_file_with_extension(MEASURE_IN_PROGRESS).build()


class TmpManager:
    @staticmethod
    def create_profiler_in_progress_file():
        f = open(path_to_profiler_file, "a")
        f.write("")
        f.close()

    @staticmethod
    def delete_profiler_in_progress_file():
        if os.path.exists(path_to_profiler_file):
            os.remove(path_to_profiler_file)

    @staticmethod
    def create_measure_in_progress_file(pid_process_to_track_cpu):
        f = open(path_to_profiler_file, "a")
        f.write(str(pid_process_to_track_cpu))
        f.close()

    @staticmethod
    def delete_measure_in_progress_file():
        if os.path.exists(path_to_profiler_file):
            os.remove(path_to_profiler_file)

    @staticmethod
    def profiler_in_progress_file_exist():
        return os.path.exists(path_to_profiler_file)

    @staticmethod
    def measure_in_progress_file_exist():
        return os.path.exists(path_to_measure_file)

    @staticmethod
    def get_pid_from_measure_in_progress_file():
        return TmpManager.__read_pid_from_pidfile(path_to_measure_file)

    @staticmethod
    def __read_pid_from_pidfile(pidfile_path):
        """ Read the PID recorded in the named PID file.

            Read and return the numeric PID recorded as text in the named
            PID file. If the PID file cannot be read, or if the content is
            not a valid PID, return ``None``.

            """
        pid = None
        try:
            pidfile = open(pidfile_path, 'r')
        except IOError:
            pass
        else:
            # According to the FHS 2.3 section on PID files in /var/run:
            #
            #   The file must consist of the process identifier in
            #   ASCII-encoded decimal, followed by a newline character.
            #
            #   Programs that read PID files should be somewhat flexible
            #   in what they accept; i.e., they should ignore extra
            #   whitespace, leading zeroes, absence of the trailing
            #   newline, or additional lines in the PID file.

            line = pidfile.readline().strip()
            try:
                pid = int(line)
            except ValueError:
                pass
            pidfile.close()

        return pid
