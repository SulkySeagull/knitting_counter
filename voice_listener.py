import queue
import json
import sounddevice as sd
from vosk import Model, KaldiRecognizer


class Listener:
    def __init__(self, handler, speaker):
        self.handler = handler
        self.speaker = speaker
        self.model = Model("vosk-model-en-us-0.22-lgraph")
        self.sample_rate = 16000
        self.q = queue.Queue()
        self.rec = KaldiRecognizer(self.model, self.sample_rate)
        self.set_command_grammer()
        self.running = True

    def callback(self, indata, frames, time, status):
        self.q.put(bytes(indata))

    def start(self):
        print("Listening... please press control Ctrl + C to stop ")
        try:
            with sd.RawInputStream(
                samplerate=self.sample_rate,
                blocksize=2500,
                dtype="int16",
                channels=1,
                callback=self.callback,
            ):
                while self.running == True:
                    data = self.q.get()
                    if self.rec.AcceptWaveform(data):
                        result = json.loads(self.rec.Result())
                        command = result["text"]

                        # If there is a verbal command
                        if command and "[unk]" not in command:
                            print(command)
                            response = self.handler.process_command(command)
                            if isinstance(response, tuple):
                                signal, message = response
                                if signal == "OPEN GRAMMAR":
                                    self.set_open_grammer()
                                # Otherwise switch back to set commands
                                else:
                                    self.set_command_grammer()
                                print(f"DEBUG speaker type: {type(self.speaker)}")
                                self.speaker.say(message)
                            else:
                                self.speaker.say(response)

                        while self.q.empty() == False:
                            self.q.get()

        except KeyboardInterrupt:
            print("\nStopped listening")
        except Exception as e:
            # print("Error in Voice Listener:", e)
            import traceback

            traceback.print_exc()

    def stop(self):
        self.running = False

    def set_command_grammer(self):
        self.rec.SetGrammar(
            '["add row", "frog row", "row count", "new project", "create project", "delete project", "trash project", "row count", "yes", "no","current project", "delete", "cancel", "list all projects", "[unk]"]'
        )

    def set_open_grammer(self):
        self.rec = KaldiRecognizer(self.model, self.sample_rate)

    #Set grammer to be project names. Used when switching projects NEEDS TESTING
    def set_project_name_grammer(self):
         grammer_string = '["'
         names = list(self.projects.keys())
         names_string = ", ".join(names)
         grammer_string += names_string
         print(grammer_string)     
    