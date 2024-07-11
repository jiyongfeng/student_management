on run {input, parameters}
    -- Ensure input path is provided
    if (count of input) is 0 then
        display dialog "No input path provided."
        return
    end if

    set sourceFolder to POSIX file (item 1 of input as string)
    set destDir to POSIX file "/Users/jiyongfeng/Documents"

    -- Define target folder names
    set folderNames to {"Images", "Softwares", "Musics", "Documents", "Others"}

    -- Create target folders
    tell application "Finder"
        repeat with folderName in folderNames
            set folderPath to ((POSIX path of destDir) & "/" & folderName) as POSIX file
            if not (exists folder folderPath) then
                try
                    make new folder at destDir with properties {name:folderName}
                on error errMsg number errNum
                    display dialog "Error: " & errMsg & " (Error number: " & errNum & ")"
                end try
            end if
        end repeat
    end tell

    -- Traverse files and move based on type
    tell application "Finder"
        set sourceFileList to every file of folder sourceFolder
        repeat with aFile in sourceFileList
            set fileName to name of aFile
            set fileExtension to name extension of aFile

            -- Set target folder path
            if fileExtension is in {"jpg", "jpeg", "png", "gif", "bmp", "tiff"} then
                set destFolder to folder "Images" of folder (destDir as alias)
            else if fileExtension is in {"mp3", "wav", "aac", "flac"} then
                set destFolder to folder "Musics" of folder (destDir as alias)
            else if fileExtension is in {"pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx", "txt"} then
                set destFolder to folder "Documents" of folder (destDir as alias)
            else if fileExtension is "dmg" then
                set destFolder to folder "Softwares" of folder (destDir as alias)
            else
                set destFolder to folder "Others" of folder (destDir as alias)
            end if

            -- Check if file exists in target location and delete if so
            set destFile to (POSIX path of (destFolder as alias)) & fileName
            if exists POSIX file destFile then
                try
                    delete POSIX file destFile
                end try
            end if

            -- Move file
            move aFile to destFolder
        end repeat
    end tell

    return input
end run