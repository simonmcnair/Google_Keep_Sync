#Import a directory of text files as google keep notes.
#Text Filename is used for the title of the note.

import gkeepapi, os, time, shutil

username = 'username@gmail.com'
password = 'google-app-password'

keep = gkeepapi.Keep()
success = keep.login(username,password)
#dir_path = os.path.dirname(os.path.realpath(__file__))
#dir_path = os.getcwd()
dir_path = 'z:/Documents/Simon/TXT'
done_folder_path = os.path.join(dir_path, 'done')


for root, dirs, files in os.walk(dir_path):
    for file in files:

        if done_folder_path in dirs:
            dirs.remove(done_folder_path)
    
        base_filename = os.path.basename(file)

        fn = os.path.join(dir_path,file)
        print("Processing " + fn)
        if os.path.isfile(fn) and fn.endswith('.txt'):
            try:
                print("Processing 2" + fn)
                # Use the file name as the note title
                title = 'Imported-' + os.path.splitext(file)[0]
                # Read the content of the TXT file
                with open(fn, 'r') as file:
                    content = file.read()

                # Set the note content
                new_note = keep.createNote(title,content)
                print("note id is " + str(new_note.id))
                keep.sync()
                if new_note.id:
                    # Create the subfolders within the "done" folder if they don't exist
                    relative_path = os.path.relpath(root, dir_path)
                    if root == dir_path:
                        relative_path = ''

                    subfolder_path = os.path.join(done_folder_path, relative_path)
                    if not os.path.exists(subfolder_path):
                        os.makedirs(subfolder_path, exist_ok=True)

                    # Move the file to the appropriate subfolder within the "done" folder
                    destination_path = os.path.join(subfolder_path, base_filename)
                    
                    #destination_path = os.path.join(subfolder_path, os.path.splitext(os.path.basename(file))[0])
                    shutil.move(os.path.join(root, base_filename), destination_path)
                    print(f"Note created and file '{fn}' moved to 'done' folder")
                else:
                    print(f"Failed to create note for file '{fn}'")
            except Exception as e:
                    print("ErRoR" + str(e))
        else:
            print("not a text file " + fn)
        time.sleep(5)
