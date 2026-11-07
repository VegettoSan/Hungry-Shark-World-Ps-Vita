using System;
using System.IO;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

// Private VPK 3 observation. Does not complete callbacks, suppress errors or edit saves.
public sealed class HSWPSP2BootDiagnostics : MonoBehaviour
{
    static HSWPSP2BootDiagnostics instance;
    StreamWriter writer;
    readonly Queue<string> recent = new Queue<string>();
    readonly HashSet<string> errors = new HashSet<string>();
    string last = "BOOT", completed = "none", firstError = "", fileStatus = "not opened";
    string memory = "not sampled", overlay = "";
    GUIStyle style;
    int records, frames;
    float start, nextMemory, updates;
    string state = "";

    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.BeforeSceneLoad)]
    static void Begin()
    {
#if UNITY_PSP2 && HSW_PSP2_BOOT_LOG
        if (instance != null) return;
        HSWPSP2FrameLimit.Apply();
        var go = new GameObject("HSW VPK3 startup diagnosis");
        DontDestroyOnLoad(go);
        instance = go.AddComponent<HSWPSP2BootDiagnostics>();
        instance.start = Time.realtimeSinceStartup;
        Application.logMessageReceived += instance.Log;
        SceneManager.sceneLoaded += instance.Scene;
        SceneManager.sceneUnloaded += instance.Unloaded;
        try {
            string directory = Application.persistentDataPath;
            if (string.IsNullOrEmpty(directory)) throw new IOException("empty persistent path");
            Directory.CreateDirectory(directory);
            string path = Path.Combine(directory, "HSW_VPK03_" + DateTime.UtcNow.ToString("yyyyMMdd_HHmmss") + "_" + Guid.NewGuid().ToString("N").Substring(0,8) + ".log");
            instance.writer = new StreamWriter(new FileStream(path, FileMode.CreateNew, FileAccess.Write, FileShare.Read));
            instance.writer.AutoFlush = true;
            instance.fileStatus = "persistent OK";
        } catch (Exception ex) { instance.fileStatus = "persistent " + ex.GetType().Name; }
        Mark("BOOT 00.03 Unity=" + Application.unityVersion + " API=" + SystemInfo.graphicsDeviceType + " " + instance.fileStatus);
        instance.Write("PATH persistent=" + Application.persistentDataPath + " data=" + Application.dataPath);
#endif
    }
    [System.Diagnostics.Conditional("HSW_PSP2_BOOT_LOG")]
    public static void Mark(string stage)
    {
        if (instance == null) return;
        instance.last = stage;
        if (stage.StartsWith("DONE ")) instance.completed = stage.Substring(5);
        instance.recent.Enqueue(stage);
        while (instance.recent.Count > 4) instance.recent.Dequeue();
        instance.SampleMemory();
        instance.Write("STAGE " + stage + " | " + instance.memory);
        instance.RefreshOverlay();
    }
    void Write(string message)
    {
        if (records++ >= 1500) return;
        string line = "[HSW_VPK03] " + Time.realtimeSinceStartup.ToString("F2") + " f=" + Time.frameCount + " " + message;
        UnityEngine.Debug.Log(line); // Retain Unity/TTY even when persistent storage fails.
        if (writer == null) return;
        try { writer.WriteLine(line); }
        catch (Exception ex) {
            fileStatus = "write " + ex.GetType().Name;
            try { writer.Dispose(); } catch { }
            writer = null;
        }
    }
    void Log(string message, string stack, LogType type)
    {
        if (message.StartsWith("[HSW_VPK03]")) return;
        if (type != LogType.Exception && type != LogType.Error && type != LogType.Assert) return;
        string bounded = message.Substring(0, Math.Min(800, message.Length));
        if (errors.Count >= 12 || !errors.Add(bounded)) return;
        if (firstError.Length == 0) firstError = bounded;
        Write("ERROR after=" + last + " " + bounded + "\n" + stack.Substring(0, Math.Min(2400, stack.Length)));
        RefreshOverlay();
    }
    void SampleMemory()
    {
        try {
#if UNITY_PSP2 && !UNITY_EDITOR
            memory = "LPDDR=" + UnityEngine.PSVita.Diagnostics.GetFreeMemoryLPDDR() +
                " CDRAM=" + UnityEngine.PSVita.Diagnostics.GetFreeMemoryCDRAM() +
                " PHYSCONT=" + UnityEngine.PSVita.Diagnostics.GetFreeMemoryPHYSCONT();
#else
            memory = "Editor: no Vita memory measurement";
#endif
            memory += " managed=" + GC.GetTotalMemory(false);
        } catch (Exception ex) { memory = "memory " + ex.GetType().Name; }
    }
    void Scene(Scene scene, LoadSceneMode mode)
    {
        HSWPSP2FrameLimit.Apply();
        Mark("DONE scene " + scene.name + " " + mode + " quality=" + QualitySettings.GetQualityLevel());
    }
    void Unloaded(Scene scene) { Mark("DONE unload " + scene.name); }
    void Update()
    {
        ++frames;
        float elapsed = Time.realtimeSinceStartup - start;
        if (elapsed < 2) return;
        updates = frames / elapsed;
        frames = 0; start = Time.realtimeSinceStartup;
        if (Application.targetFrameRate != 60 || QualitySettings.vSyncCount != 1) {
            Write("CAP drift target=" + Application.targetFrameRate + " vsync=" + QualitySettings.vSyncCount);
            HSWPSP2FrameLimit.Apply();
        }
        // Observe the existing state machine without instantiating a singleton.
        var machine = GameStateMachine.GameStateMachineInstance;
        if (machine != null && machine.GetCurrentState() != null) {
            string current = machine.GetCurrentState().name;
            if (current != state) { state = current; Mark("STATE " + state); }
        }
        if (Time.realtimeSinceStartup >= nextMemory && Time.realtimeSinceStartup <= 90) {
            nextMemory = Time.realtimeSinceStartup + 5;
            SampleMemory(); Write("ALIVE target=" + Application.targetFrameRate + " vsync=" + QualitySettings.vSyncCount + " Update/s=" + updates.ToString("F1") + " " + memory);
        }
        RefreshOverlay();
    }
    void RefreshOverlay()
    {
        overlay = "HSW VPK 3 / 00.03  target=" + Application.targetFrameRate + " vsync=" + QualitySettings.vSyncCount +
            " Update/s=" + updates.ToString("F1") + " (not scanout) | " + fileStatus + "\n" +
            string.Join(" > ", recent.ToArray()) + "\nLast completed: " + completed + "\n" + memory;
        if (firstError.Length > 0) overlay += "\nERROR: " + firstError.Substring(0, Math.Min(240, firstError.Length));
    }
    void OnGUI()
    {
        if (style == null) { style = new GUIStyle(GUI.skin.box); style.fontSize = 13; style.alignment = TextAnchor.UpperLeft; style.wordWrap = true; }
        GUI.depth = -2000;
        GUI.Box(new Rect(4, 4, Screen.width - 8, firstError.Length == 0 ? 115 : 155), overlay, style);
    }
    void OnApplicationPause(bool paused) { Mark("LIFECYCLE pause=" + paused); }
    void OnApplicationQuit() { Mark("LIFECYCLE quit"); }
    void OnDestroy()
    {
        if (instance != this) return;
        Application.logMessageReceived -= Log;
        SceneManager.sceneLoaded -= Scene;
        SceneManager.sceneUnloaded -= Unloaded;
        if (writer != null) writer.Dispose();
        instance = null;
    }
}
