using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class random_animation : MonoBehaviour
{
    // Reference to the Animator
    private Animator animator;

    // List of animation state names as strings
    public string[] animationStates;

    // Time to wait before changing animation
    public float timeBetweenAnimations = 0.5f; // seconds

    private float timer;

    void Start()
    {
        // Get the Animator component attached to the GameObject
        animator = GetComponent<Animator>();

        // Start playing the first random animation immediately
        PlayRandomAnimation();
    }

    void Update()
    {
        // Timer to control the interval between animations
        timer += Time.deltaTime;

        if (timer >= timeBetweenAnimations)
        {
            PlayRandomAnimation();
            timer = 0f; // Reset the timer
        }
    }

    void PlayRandomAnimation()
    {
        // Pick a random animation from the list of state names
        int randomIndex = Random.Range(0, animationStates.Length);
        string randomAnimation = animationStates[randomIndex];

        // Trigger the animation in the Animator
        animator.Play(randomAnimation);
    }
}

