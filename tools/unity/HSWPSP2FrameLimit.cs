using UnityEngine;
using UnityEngine.SceneManagement;

// Presentation only. Keep the original simulation clock, physics and animation.
public static class HSWPSP2FrameLimit
{
    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.BeforeSceneLoad)]
    static void Boot()
    {
#if UNITY_PSP2
        Apply();
        SceneManager.sceneLoaded -= SceneLoaded;
        SceneManager.sceneLoaded += SceneLoaded;
#endif
    }
    static void SceneLoaded(Scene scene, LoadSceneMode mode) { Apply(); }
    public static void Apply()
    {
#if UNITY_PSP2
        QualitySettings.vSyncCount = 1;
        Application.targetFrameRate = 60;
#endif
    }
}
