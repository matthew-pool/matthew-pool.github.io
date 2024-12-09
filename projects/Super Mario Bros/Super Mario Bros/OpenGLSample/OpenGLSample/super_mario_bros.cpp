/**
 * super_mario_bros.cpp
 * Modern OpenGL
 * @author: Matthew Pool
 * @date: December 10, 2023
 * @brief: Popular scene from Nintendo's 1985 video game "Super Mario Bros."
 * @attribution: Professor Scott Gray (SNHU): https://github.com/scottmgray
 * created original "createPrism" function used in this file.
 * 
 */
// TODO: animated goomba overlay (transparent PNG/RGBA) on X-Y background
//---------------------------------------------------------------------
// include files
//---------------------------------------------------------------------
#include <iostream>         // cout, cerr
#include <cstdlib>          // EXIT_FAILURE
#include <iomanip>          // setprecision
#include <vector>           
#include <../include/GLAD/glad/glad.h>      // GLAD library
#include <../include/GLFW/include/GLFW/glfw3.h>     // GLFW library

// GLM Math Header inclusions
#include <../include/glm/glm/glm.hpp>
//#include <glm/gtc/matrix_transform.hpp>
#include <../include/glm/glm/gtx/transform.hpp>
#include <../include/glm/glm/gtc/type_ptr.hpp>

#include "shader.h"
#include "camera.h"
//#include "mesh.h"

// textures
#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"  // stbi_load image loader function

using namespace std; // standard namespace
//---------------------------------------------------------------------
// unnamed namespace
//---------------------------------------------------------------------
namespace
{
    struct Mesh
    {
        GLuint vao; // vertex array
        GLuint vbo; // verts (x,y,z,nx,ny,nz,u,t)
        GLuint ebo; // indices
        GLuint vertexBytes;
        GLuint indexBytes;
        vector<GLfloat> verts;
        vector<GLushort> indices;

        Mesh() : vao(0), vbo(0), ebo(0), vertexBytes(0), indexBytes(0) {}  // default constructor

        ~Mesh()  // destructor
        {
            if (vao != 0)
                glDeleteVertexArrays(1, &vao);
            if (vbo != 0)
                glDeleteBuffers(1, &vbo);
            if (ebo != 0)
                glDeleteBuffers(1, &ebo);
        }
    };
    //---------------------------------------------------------------------
    // mesh initializations
    //---------------------------------------------------------------------
    Mesh goombaMesh, hillMesh, backgroundMesh, textMesh, blockMesh, poleMesh, flagMesh, groundMesh, bottomPipeMesh, topPipeMesh;
    vector<Mesh> meshes = { goombaMesh, hillMesh, backgroundMesh, textMesh, blockMesh, poleMesh, flagMesh, groundMesh, bottomPipeMesh, topPipeMesh };
    GLuint goombaTextureId0, goombaTextureId1, goombaTextureId2, hillTextureId, backgroundTextureId, textTextureId, blockTextureId, poleTextureId, flagTextureId, groundTextureId, pipeTextureId;
    vector<GLuint> textureIds = { goombaTextureId0, goombaTextureId1, goombaTextureId2, hillTextureId, backgroundTextureId, textTextureId, blockTextureId, poleTextureId, flagTextureId, groundTextureId, pipeTextureId };
    //---------------------------------------------------------------------
    // global constants/variables
    //---------------------------------------------------------------------
    const GLuint floatsPerPosition = 3;
    const GLuint floatsPerNormal = 3;
    //const GLuint floatsPerColor = 4;
    const GLuint floatsPerTexture = 2;
    const GLuint floatsPerVertex = floatsPerPosition + floatsPerNormal + floatsPerTexture;
    const int STRIDE = sizeof(float) * floatsPerVertex;
    //---------------------------------------------------------------------
    // sizes/positions
    //---------------------------------------------------------------------
    float scaleFactor = 1.0f;
    float length, halfLen = 0.0f;
    const float yGround = -0.75f;     // y position of the ground plane
    float x = 0.0f; // x offset
    float y = 0.0f; // y offset
    float z = 0.0f; // z offset
    //---------------------------------------------------------------------
    // window attributes
    //---------------------------------------------------------------------
    GLFWwindow* window = nullptr;
    const char* const WINDOW_TITLE = "Super Mario Bros.";
    const int WINDOW_WIDTH = 1024; // 16:9 widescreen ratio
    const int WINDOW_HEIGHT = 768; // 720p HD resolution
    const float ASPECT_RATIO = (float)WINDOW_WIDTH / (float)WINDOW_HEIGHT;
    float lastX = WINDOW_WIDTH / 2.0f;  // last x-position of mouse
    float lastY = WINDOW_HEIGHT / 2.0f; // last y-position of mouse
    bool firstMouse = true;
    bool yCheck = true;
    bool repositionText = true;
    bool firstLoop = true;
    //---------------------------------------------------------------------
    // camera/view initial settings
    //---------------------------------------------------------------------
    float depth = 3.0f;     // z position of the camera for the ortho projection
    Camera camera(glm::vec3(0.0f, 0.0f, depth));
    glm::vec3 cameraPos = glm::vec3(0.0f, 0.0f, -depth);
    glm::vec3 cameraFront = glm::vec3(0.0f, 0.0f, -1.0f);
    glm::vec3 cameraUp = glm::vec3(0.0f, 1.0f, 0.0f);
    bool littleMario = false;
    //---------------------------------------------------------------------
    // ortho settings
    //---------------------------------------------------------------------
    bool isOrtho = false;  // 'P' toggle for orthographic projection or perspective projection
    float frustumHeight = 2.0f * depth * tan(glm::radians(camera.Zoom) / 2.0f);
    float frustumWidth = frustumHeight * ASPECT_RATIO;
    float orthoLeft = -frustumWidth / 2.0f;
    float orthoRight = frustumWidth / 2.0f;
    float orthoBottom = -frustumHeight / 2.0f;
    float orthoTop = frustumHeight / 2.0f;
    float nearPlane = 0.1f; // clipping plane
    float farPlane = 10.0f; // clipping plane
    //---------------------------------------------------------------------
    // time
    //---------------------------------------------------------------------
    float deltaTime = 0.0f; // time between current frame and last frame
    float currentFrame = 0.0f;
    float lastFrame = 0.0f;
}   // end namespace
//---------------------------------------------------------------------
// function prototypes
//---------------------------------------------------------------------
bool UInitialize(int, char* [], GLFWwindow** window);
void UResizeWindow(GLFWwindow* window, int width, int height);
void URender(Shader shader);  // view/projection matrices & object rendering
bool UCreateTexture(const char* filename, GLuint& textureId); // load image file and set texture settings
//---------------------------------------------------------------------
void processInput(GLFWwindow* window);
void mouseScrollCallback(GLFWwindow* window, double xoffset, double yoffset);
void mousePositionCallback(GLFWwindow* window, double xpos, double ypos);
void mouseButtonCallback(GLFWwindow* window, int button, int action, int mods);
//---------------------------------------------------------------------
void cleanUp();
void createVertexArray(Mesh& mesh);
void createGoomba(Mesh& mesh);
void createHill(Mesh& mesh);
void createBackground(Mesh& mesh);
void createGround(Mesh& mesh);
void createFlag(Mesh& mesh);
void createText(Mesh& mesh);
void createBlock(Mesh& mesh);
void createPole(Mesh& mesh);
void createBottomPipe(Mesh& mesh);
void createTopPipe(Mesh& mesh);
void createPrism(Mesh& mesh, int numSides, float radius, float halfLen);
//---------------------------------------------------------------------
// Main function
//---------------------------------------------------------------------
int main(int argc, char* argv[])
{
    if (!UInitialize(argc, argv, &window))
        return EXIT_FAILURE;
    //---------------------------------------------------------------------
    // mesh vao, vbo, ebo, model matrix creation/binding
    //---------------------------------------------------------------------
    //createGoomba(goombaMesh);
    createHill(hillMesh);
    createBackground(backgroundMesh);
    createGround(groundMesh);
    createFlag(flagMesh);
    createText(textMesh);
    createBlock(blockMesh);
    createPole(poleMesh);
    createBottomPipe(bottomPipeMesh);
    createTopPipe(topPipeMesh);
    //---------------------------------------------------------------------
    // shader.h shader program creation
    //---------------------------------------------------------------------
    Shader lightingShader("../OpenGLSample/shaderfiles/lightingShader.vs", "../OpenGLSample/shaderfiles/lightingShader.fs");
    lightingShader.use();  // shader does not accept color input (x,y,z,nx,ny,nz,u,t)
    //---------------------------------------------------------------------
    // texture creation
    //---------------------------------------------------------------------
    const char* filename;

    /*
    // goombaTexture (goombaTextureIds)
    filename = "../OpenGLSample/images/goomba_texture0.png";
     if (!UCreateTexture(filename, goombaTextureId0))
         cout << "Failed to load texture" << endl;
    filename = "../OpenGLSample/images/goomba_texture1.png";
     if (!UCreateTexture(filename, goombaTextureId1))
         cout << "Failed to load texture" << endl;
    filename = "../OpenGLSample/images/goomba_texture2.png";
     if (!UCreateTexture(filename, goombaTextureId2))
         cout << "Failed to load texture" << endl;
    */

    // hillTexture (hillTextureId)
    filename = "../OpenGLSample/images/hill_texture.jpg";
    if (!UCreateTexture(filename, hillTextureId))
        cout << "Failed to load texture" << endl;

    // backgroundTexture (backgroundTextureId)
    filename = "../OpenGLSample/images/background_texture2.jpg";
    if (!UCreateTexture(filename, backgroundTextureId))
        cout << "Failed to load texture" << endl;

    // groundTexture (groundTextureId)
    filename = "../OpenGLSample/images/ground_texture2.jpg";
    if (!UCreateTexture(filename, groundTextureId))
        cout << "Failed to load texture" << endl;

    // flagTexture (flagTextureId)
    filename = "../OpenGLSample/images/flag_overlay4.png";
    if (!UCreateTexture(filename, flagTextureId))
        cout << "Failed to load texture" << endl;

    // textTexture (textTextureId)
    filename = "../OpenGLSample/images/text_texture.png";
    if (!UCreateTexture(filename, textTextureId))
        cout << "Failed to load texture" << endl;

    // blockTexture (blockTextureId)
    filename = "../OpenGLSample/images/block_texture.jpg"; //block_texture2.jpg; //brick_texture.jpg;
    if (!UCreateTexture(filename, blockTextureId))
        cout << "Failed to load texture" << endl;

    // poleTexture (poleTextureId)
    filename = "../OpenGLSample/images/pole_texture.jpg";
    if (!UCreateTexture(filename, poleTextureId))
        cout << "Failed to load texture" << endl;

    // pipeTexture (pipeTextureId)
    filename = "../OpenGLSample/images/pipe_texture.jpg";
    if (!UCreateTexture(filename, pipeTextureId))
        cout << "Failed to load texture" << endl;

    //---------------------------------------------------------------------
    // set background clear color
    glClearColor(0.0f, 0.0f, 0.0f, 1.0f);  // black

    // enable z-depth
    glEnable(GL_DEPTH_TEST);
    //---------------------------------------------------------------------
    // render loop
    //---------------------------------------------------------------------
    while (!glfwWindowShouldClose(window))
    {
        // clear frame and z-buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

        // per-frame time logic
        currentFrame = glfwGetTime();
        deltaTime = currentFrame - lastFrame; // time since last frame
        lastFrame = currentFrame;

        // user input
        processInput(window);

        // render single frame
        URender(lightingShader);

        // flips back buffer with front buffer every frame
        glfwSwapBuffers(window);

        glfwPollEvents();
    }   // end render loop

    //---------------------------------------------------------------------
    // cleanup resources
    //---------------------------------------------------------------------
    cleanUp();  // destroys meshes (vao/vbo/ebo) and textures
    glDeleteShader(lightingShader.ID);
    glDeleteProgram(lightingShader.ID);
    glBindVertexArray(0);               // unbind vertex array
    glActiveTexture(GL_TEXTURE0);       
    glBindTexture(GL_TEXTURE_2D, 0);    // unbind texture
    glActiveTexture(GL_TEXTURE1);
    glBindTexture(GL_TEXTURE_2D, 0);    // unbind texture
    glUseProgram(0);                    // unbind shader program
    glfwDestroyWindow(window);
    glfwTerminate();

    return EXIT_SUCCESS;
    //exit(EXIT_SUCCESS); // terminates the program successfully
}   // end main()
//---------------------------------------------------------------------
// render single frame
//---------------------------------------------------------------------
void URender(Shader shader)
{
    //---------------------------------------------------------------------
    // view/projection matrices
    //---------------------------------------------------------------------
    glm::mat4 view;
    view = camera.GetViewMatrix();  // camera.h handles view matrix to allow movement
    //glm::mat4 view = glm::translate(glm::vec3(0.0f, 0.0f, -5.0f));
    //glm::mat4 view = glm::translate(glm::vec3(camera.Position));

    glm::mat4 projection;
    if (isOrtho)  // orthographic projection
        projection = glm::ortho(orthoLeft, orthoRight, orthoBottom, orthoTop, nearPlane, farPlane); // orthographic projection
    else  // perspective projection
        // Projection Matrix (FoV, ratio, display range=0.1->100.0 units)
        projection = glm::perspective(glm::radians(camera.Zoom), ASPECT_RATIO, nearPlane, farPlane);  // perspective projection
    //glm::mat4 projection = glm::perspective(glm::radians(45.0f), 4.0f / 3.0f, 0.1f, 100.0f);
    //glm::mat4 projection = glm::perspective(glm::radians(45.0f), ASPECT_RATIO, 0.1f, 100.0f);

    shader.use();

    shader.setMat4("projection", projection);
    shader.setMat4("view", view);
    if (littleMario)  // low camera
        camera.Position.y = yGround + 0.1f;  // little Mario eye-level
    //shader.setVec3("viewPos", camera.Position);

    //shader.setBool("useOverlay", false);  // default to no overlay image
    //---------------------------------------------------------------------
    //  light settings
    //---------------------------------------------------------------------
    // CUSTOMIZE lightingShader.fs:
        // #define NUM_POINT_LIGHTS = 1 to 4
        // comment out "results += ..." for each light type not used

    float xDir;
    float yDir;
    float zDir;
    float xPos;
    float yPos;
    float zPos;

    // Phong lighting model
    // set colors and intensity of each light type
    
    // directional light (100% white)
    xDir = -0.0f; //-0.5f;
    yDir = -1.0f; //-0.5f;
    zDir = -1.0f; //-0.15f;
    shader.setVec3("dirLight.direction", xDir, yDir, zDir);
    shader.setVec3("dirLight.ambient", 1.0f, 1.0f, 1.0f);   // base color in indirect light
    shader.setVec3("dirLight.diffuse", 1.0f, 1.0f, 1.0f);   // surface scatter (glossy/matte) and primary color in direct light
    shader.setVec3("dirLight.specular", 1.0f, 1.0f, 1.0f);  // highlights (bright spots) intensity based on lamp and camera angle

    // point light (100% warm yellow)
    xPos = 0.75f;
    yPos = 0.25f;
    zPos = -0.5f;
    const glm::vec3 warmYellow = glm::vec3(1.0f, 0.87f, 0.0f);
    const glm::vec3 brightYellow = glm::vec3(1.0f, 1.0f, 0.88f);
    const glm::vec3 brightWhite = glm::vec3(1.0f, 1.0f, 1.0f);
    shader.setVec3("pointLights[0].position", xPos, yPos, zPos);
    shader.setVec3("pointLights[0].ambient", warmYellow);  
    shader.setVec3("pointLights[0].diffuse", 1.0f, 1.0f, 1.0f);
    shader.setVec3("pointLights[0].specular", 1.0f, 1.0f, 1.0f);
    shader.setFloat("pointLights[0].constant", 1.0f);    // base level of light that doesn't diminish
    shader.setFloat("pointLights[0].linear", 0.09f);	 // rate of light diminshment over distance
    shader.setFloat("pointLights[0].quadratic", 0.032f); // rate of light diminshment over distance squared

    // point light (50% red)
    xPos = 1.4f; // centered with flag pole
    yPos = yGround + 0.555f; // top of pole
    zPos = 0.0f;
    /*
    shader.setVec3("pointLights[1].position", xPos, yPos, zPos);
    shader.setVec3("pointLights[1].ambient", 0.5f, 0.0f, 0.0);
    shader.setVec3("pointLights[1].diffuse", 1.0f, 0.0f, 0.0f); 
    shader.setVec3("pointLights[1].specular", 1.0f, 1.0f, 1.0f); 
    shader.setFloat("pointLights[1].constant", 1.0f);   
    shader.setFloat("pointLights[1].linear", 0.09f);	
    shader.setFloat("pointLights[1].quadratic", 0.032f); 
    */

    // spot light (100% red)
    xPos = xPos + 0.05f;
    yPos = yPos + 0.05f;  //+ 0.01f; // - 0.01f;
    zPos = -0.05f;
    xDir = -0.05f;
    yDir = -1.0f; //1.0f;
    zDir = 0.05f;
    /*
    //shader.setVec3("spotLight.position", camera.Position);
    //shader.setVec3("spotLight.direction", camera.Front);
    shader.setVec3("spotLight.position", xPos, yPos, zPos);
    shader.setVec3("spotLight.direction", xDir, -yDir, zDir);
    shader.setFloat("spotLight.cutOff", glm::cos(glm::radians(12.5f)));
    shader.setFloat("spotLight.outerCutOff", glm::cos(glm::radians(15.0f)));
    shader.setVec3("spotLight.ambient", 1.0f, 0.0f, 0.0f);
    shader.setVec3("spotLight.diffuse", 1.0f, 0.0f, 0.0f);
    shader.setVec3("spotLight.specular", 1.0f, 1.0f, 1.0f);
    shader.setFloat("spotLight.constant", 1.0f);
    shader.setFloat("spotLight.linear", 0.09f);
    shader.setFloat("spotLight.quadratic", 0.032f);
    */

    // point light (25% green)
    xPos = -1.225f; // centered with pipe
    yPos = yGround + 0.12f / 2.0f * 3.0f; // top of pipe
    zPos = 0.0;
    /*
    // TODO: change to pointLights[2] if using 3+ point lights
    shader.setVec3("pointLights[1].position", xPos, yPos, zPos);
    shader.setVec3("pointLights[1].ambient", 0.0f, 0.5f, 0.0);  
    shader.setVec3("pointLights[1].diffuse", 0.0f, 0.25f, 0.0f);  
    shader.setVec3("pointLights[1].specular", 0.0f, 0.25f, 0.0f); 
    shader.setFloat("pointLights[1].constant", 1.0f);   
    shader.setFloat("pointLights[1].linear", 0.09f);	
    shader.setFloat("pointLights[1].quadratic", 0.032f); 
    */

    // spot light (100% green)
    xPos = xPos + 0.25f;
    yPos = yPos + 0.01f; //- 0.01f;
    zPos = 0.5f;
    xDir = -0.25f;
    yDir = yDir; //-yDir;
    zDir = 0.5f;
    //shader.setVec3("spotLight.position", camera.Position);
    //shader.setVec3("spotLight.direction", camera.Front);
    shader.setVec3("spotLight.position", xPos, yPos, zPos);
    shader.setVec3("spotLight.direction", xDir, -yDir, zDir);
    shader.setFloat("spotLight.cutOff", glm::cos(glm::radians(12.5f)));
    shader.setFloat("spotLight.outerCutOff", glm::cos(glm::radians(15.0f)));
    shader.setVec3("spotLight.ambient", 0.0f, 1.0f, 0.0f);
    shader.setVec3("spotLight.diffuse", 0.0f, 1.0f, 0.0f);
    shader.setVec3("spotLight.specular", 1.0f, 1.0f, 1.0f);
    shader.setFloat("spotLight.constant", 1.0f);
    shader.setFloat("spotLight.linear", 0.09f);
    shader.setFloat("spotLight.quadratic", 0.032f);
    
    //---------------------------------------------------------------------
    // draw objects
    //---------------------------------------------------------------------
    glm::mat4 rotate, translate, scale;
    glm::mat4 model = glm::mat4(1.0f); // identity matrix
    //---------------------------------------------------------------------
    // Hill
    //---------------------------------------------------------------------
    scaleFactor = 0.75f;
    scale = glm::scale(glm::vec3(scaleFactor, scaleFactor, scaleFactor));
    rotate = glm::rotate(0.0f, glm::vec3(0.0f, 1.0f, 0.0f));
    translate = glm::translate(glm::vec3(0.775f, yGround, -1.0f));
    model = translate * rotate * scale;
    shader.setMat4("model", model);  // send model matrix to shader

    shader.setFloat("material.shininess", 30.0f);   // low shine matte surface
    shader.setVec3("material.diffuse", 0.3f, 0.8f, 0.3f);   // greenish tone
    shader.setVec3("material.specular", 0.3f, 0.8f, 0.3f);  // low reflectivity
    glActiveTexture(GL_TEXTURE0);  // GL_TEXTURE1 for transparent PNG overlay textures
    glBindTexture(GL_TEXTURE_2D, hillTextureId);
    glBindVertexArray(hillMesh.vao);
    glDrawElements(GL_TRIANGLES, hillMesh.indexBytes, GL_UNSIGNED_SHORT, NULL);
    //glDrawArrays(GL_TRIANGLES, 0, mesh.vertexBytes);  // switched from using indices
    //---------------------------------------------------------------------
    // Background
    //---------------------------------------------------------------------
    scaleFactor = 1.0f;
    scale = glm::scale(glm::vec3(scaleFactor, scaleFactor, scaleFactor));
    rotate = glm::rotate(0.0f, glm::vec3(0.0f, 1.0f, 0.0f));
    translate = glm::translate(glm::vec3(0.0f, 0.0f, 0.0f));
    model = translate * rotate * scale;
    shader.setMat4("model", model);

    shader.setFloat("material.shininess", 0.5f);   // low shine
    shader.setVec3("material.diffuse", 0.1f, 0.1f, 1.0f);   // blue tone
    shader.setVec3("material.specular", 0.1f, 0.1f, 1.0f);  // low reflectivity
    glActiveTexture(GL_TEXTURE0);  // GL_TEXTURE1 for transparent PNG overlay textures
    glBindTexture(GL_TEXTURE_2D, backgroundTextureId);
    glBindVertexArray(backgroundMesh.vao);
    glDrawElements(GL_TRIANGLES, backgroundMesh.indexBytes, GL_UNSIGNED_SHORT, NULL);
    //---------------------------------------------------------------------
    // Ground
    // ---------------------------------------------------------------------
    scaleFactor = 1.0f;
    scale = glm::scale(glm::vec3(scaleFactor, scaleFactor, scaleFactor));
    rotate = glm::rotate(0.0f, glm::vec3(0.0f, 1.0f, 0.0f));
    translate = glm::translate(glm::vec3(0.0f, 0.0f, 0.0f));
    model = translate * rotate * scale;
    shader.setMat4("model", model);  // send model matrix to shader

    shader.setFloat("material.shininess", 30.0f);   // low shine matte surface
    shader.setVec3("material.diffuse", 0.8f, 0.3f, 0.3f);   // reddish tone
    shader.setVec3("material.specular", 0.8f, 0.3f, 0.3f);  // low reflectivity
    glActiveTexture(GL_TEXTURE0);  // GL_TEXTURE1 for transparent PNG overlay textures
    glBindTexture(GL_TEXTURE_2D, groundTextureId);
    glBindVertexArray(groundMesh.vao);
    glDrawElements(GL_TRIANGLES, groundMesh.indexBytes, GL_UNSIGNED_SHORT, NULL);
    //---------------------------------------------------------------------
    // Flag
    //---------------------------------------------------------------------
    scaleFactor = 1.0f;
    scale = glm::scale(glm::vec3(scaleFactor, scaleFactor, scaleFactor));
    rotate = glm::rotate(0.0f, glm::vec3(0.0f, 1.0f, 0.0f));  
    translate = glm::translate(glm::vec3(1.32f, yGround + 0.915f, 0.0f)); // 0.165 = -0.75 + 0.915
    model = translate * rotate * scale;
    shader.setMat4("model", model);  // send model matrix to shader

    shader.setFloat("material.shininess", 50.0f);   // mid shine matte surface
    shader.setVec3("material.diffuse", 0.5f, 0.5f, 0.5f);   // white/gray
    shader.setVec3("material.specular", 0.5f, 0.5f, 0.5f);  // mid reflectivity
    glActiveTexture(GL_TEXTURE0);  // GL_TEXTURE1 for transparent PNG overlay textures
    glBindTexture(GL_TEXTURE_2D, flagTextureId);
    glBindVertexArray(flagMesh.vao);
    glDrawElements(GL_TRIANGLES, flagMesh.indexBytes, GL_UNSIGNED_SHORT, NULL);
    //---------------------------------------------------------------------
    // Text
    //---------------------------------------------------------------------
    if (repositionText)     // triggered when switching between ortho and perspective projection
        createText(textMesh);

    scaleFactor = 1.0f;
    scale = glm::scale(glm::vec3(scaleFactor, scaleFactor, scaleFactor));
    rotate = glm::rotate(0.0f, glm::vec3(0.0f, 1.0f, 0.0f));
    translate = glm::translate(glm::vec3(0.0f, 0.0f, 0.0f));
    model = translate * rotate * scale;
    shader.setMat4("model", model);

    shader.setFloat("material.shininess", 0.5f);   // mid shine
    shader.setVec3("material.diffuse", 1.0f, 1.0f, 1.0f);   // white tone
    shader.setVec3("material.specular", 1.0f, 1.0f, 1.0f);  // high reflectivity
    glActiveTexture(GL_TEXTURE0);  // GL_TEXTURE1 for transparent PNG overlay textures
    glBindTexture(GL_TEXTURE_2D, textTextureId);
    glBindVertexArray(textMesh.vao);
    glDrawElements(GL_TRIANGLES, textMesh.indexBytes, GL_UNSIGNED_SHORT, NULL);
    //---------------------------------------------------------------------
    // Blocks
    //---------------------------------------------------------------------
    float side = 0.105f;  // side length of each block
    float half = side / 2.0f;  // half side length of each block
    scaleFactor = 1.2f;
    scale = glm::scale(glm::vec3(scaleFactor, scaleFactor, scaleFactor));
    rotate = glm::rotate(0.0f, glm::vec3(0.0f, 1.0f, 0.0f));

    shader.setFloat("material.shininess", 30.0f);   // low shine matte surface
    shader.setVec3("material.diffuse", 0.8f, 0.3f, 0.3f);   // reddish tone
    shader.setVec3("material.specular", 0.8f, 0.3f, 0.3f);  // low reflectivity
    glActiveTexture(GL_TEXTURE0);  // GL_TEXTURE1 for transparent PNG overlay textures
    glBindTexture(GL_TEXTURE_2D, blockTextureId);
    glBindVertexArray(blockMesh.vao);

    // Base Block (Flag Pole)
    translate = glm::translate(glm::vec3(1.4f, yGround + (half * scaleFactor), 0.0f));  // (0.95f, -0.7f, 0.0f)
    model = translate * rotate * scale;  // will be overwritten right before step blocks are drawn    
    shader.setMat4("model", model); // passes blockMesh.model matrix to uniform mat4 model location in vertex shader
    glDrawElements(GL_TRIANGLES, blockMesh.indexBytes, GL_UNSIGNED_SHORT, NULL);

    // Step Blocks
    x = -6.5 * side;
    y = yGround + (half * scaleFactor);
    z = 0.0f;
    float height = 0;  // incrementing height of each subsequent column
    for (int column = 1; column <= 8; column++) // starting with bottom left step (1st 8 columns)
    {
        height++;
        y = yGround + (half * scaleFactor);  // reset y position for each column
        for (int j = 0; j < height; j++)  // 8 rows high
        {
            translate = glm::translate(glm::vec3(x, y, z));   // move down and to the right side of screen
            model = translate * rotate * scale;
            shader.setMat4("model", model);
            glDrawElements(GL_TRIANGLES, blockMesh.indexBytes, GL_UNSIGNED_SHORT, NULL);
            y += side;
        }
        x += side;
    }
    // final column
    y = yGround + (half * scaleFactor);  // reset y position for each column
    for (int i = 0; i < height; i++)  // position still 8 blocks high
    {
        translate = glm::translate(glm::vec3(x, y, z));   // move down and to the right side of screen
        model = translate * rotate * scale;
        shader.setMat4("model", model);
        glDrawElements(GL_TRIANGLES, blockMesh.indexBytes, GL_UNSIGNED_SHORT, NULL);
        y += side;
    }
    //---------------------------------------------------------------------
    // Pole
    // ---------------------------------------------------------------------
    scaleFactor = 1.0f;
    scale = glm::scale(glm::vec3(scaleFactor, scaleFactor, scaleFactor));
    rotate = glm::rotate(0.0f, glm::vec3(1.0f, 1.0f, 0.0f));
    translate = glm::translate(glm::vec3(1.4f, yGround + 0.555, 0.0f));
    model = translate * rotate * scale;
    shader.setMat4("model", model);  // send model matrix to shader

    shader.setFloat("material.shininess", 99.0f); 
    shader.setVec3("material.diffuse", 0.9f, 0.9f, 0.0f);   
    shader.setVec3("material.specular", 0.9f, 0.9f, 0.0f);  
    glActiveTexture(GL_TEXTURE0);  // GL_TEXTURE1 for transparent PNG overlay textures
    glBindTexture(GL_TEXTURE_2D, poleTextureId);
    glBindVertexArray(poleMesh.vao);
    glDrawElements(GL_TRIANGLES, poleMesh.indexBytes, GL_UNSIGNED_SHORT, NULL);
    //---------------------------------------------------------------------
    // Pipe
    // ---------------------------------------------------------------------
    shader.setFloat("material.shininess", 95.0f);   // high shine glossy surface
    shader.setVec3("material.diffuse", 0.3f, 0.8f, 0.3f);   // greenish tone
    shader.setVec3("material.specular", 0.3f, 0.8f, 0.3f);  // high reflectivity
    glActiveTexture(GL_TEXTURE0);  // GL_TEXTURE1 for transparent PNG overlay textures
    glBindTexture(GL_TEXTURE_2D, pipeTextureId);

    // Bottom Pipe
    scaleFactor = 1.0f;
    length = 0.12f;
    halfLen = length / 2.0f;
    scale = glm::scale(glm::vec3(scaleFactor, scaleFactor, scaleFactor));
    rotate = glm::rotate(0.0f, glm::vec3(0.0f, 1.0f, 0.0f));
    translate = glm::translate(glm::vec3(-1.225f, yGround + halfLen, 0.0f));
    model = translate * rotate * scale;
    shader.setMat4("model", model);  // send model matrix to shader
    glBindVertexArray(bottomPipeMesh.vao);
    glDrawElements(GL_TRIANGLES, bottomPipeMesh.indexBytes, GL_UNSIGNED_SHORT, NULL);

    // Top Pipe
    scaleFactor = 1.0f;
    scale = glm::scale(glm::vec3(scaleFactor, scaleFactor, scaleFactor));
    rotate = glm::rotate(0.0f, glm::vec3(0.0f, 1.0f, 0.0f));
    translate = glm::translate(glm::vec3(-1.225f, yGround + halfLen * 3, 0.0f));
    model = translate * rotate * scale;
    shader.setMat4("model", model);  // send model matrix to shader
    glBindVertexArray(topPipeMesh.vao);
    glDrawElements(GL_TRIANGLES, topPipeMesh.indexBytes, GL_UNSIGNED_SHORT, NULL);
    //---------------------------------------------------------------------
    // Goomba
    //---------------------------------------------------------------------
    /*
    // overlay blending / transparency
    //glDisable(GL_DEPTH_TEST);
    //glEnable(GL_BLEND);
    //glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    //shader.setBool("useOverlay", true);  // use overlay texture
    //shader.setInt("baseTexture", 0);     // base texture (JPG) at GL_TEXTURE0 (default
    //shader.setInt("overlayTexture", 1);  // overlay texture (transparent PNG) at GL_TEXTURE1
    //shader.setInt("material.diffuse", 0);
    //shader.setInt("material.specular", 1);

    // TODO: animate goomba movement and texture
    GLuint goombaTextureId;
    if (true)
        goombaTextureId = goombaTextureId0;
    else if (true)
        goombaTextureId = goombaTextureId1;
    else if (true)
        goombaTextureId = goombaTextureId2;

    scaleFactor = 1.0f;
    height = 1.0f; // goomba height
    half = height / 2.0f;
    scale = glm::scale(glm::vec3(scaleFactor, scaleFactor, scaleFactor));
    rotate = glm::rotate(0.0f, glm::vec3(0.0f, 1.0f, 0.0f));
    translate = glm::translate(glm::vec3(-0.5f, yGround + half * scaleFactor, -0.99f));
    model = translate * rotate * scale;
    shader.setMat4("model", model);

    shader.setFloat("material.shininess", 0.5f);
    shader.setVec3("material.diffuse", 0.5f, 0.5f, 0.5f);
    shader.setVec3("material.specular", 0.5f, 0.5f, 0.5f);
    glActiveTexture(GL_TEXTURE0);
    //glActiveTexture(GL_TEXTURE1);
    glBindTexture(GL_TEXTURE_2D, goombaTextureId);
    glBindVertexArray(goombaMesh.vao);
    glDrawElements(GL_TRIANGLES, goombaMesh.indexBytes, GL_UNSIGNED_SHORT, NULL);

    //shader.setBool("useOverlay", false);
    //glDisable(GL_DEPTH_TEST);
    //glDisable(GL_BLEND);
    */
    //---------------------------------------------------------------------
}   // end URender()
//---------------------------------------------------------------------
// Goomba
// ---------------------------------------------------------------------
void createGoomba(Mesh& mesh)
{
    // Goomba: square quad (plane) on X-Y plane with 2 triangles
    // v3-----v2
    // |       |
    // |       |
    // |       |
    // v0-----v1

    mesh.verts = {
		//x	    y       z       nx      ny      nz      u       v       // relV absV
		// Right Side Triangle 0-1-2 (normals point towards screen)
		-0.5f,  -0.5f,   0.0f,   0.0f,   0.0f,   1.0f,   0.0f,  0.0f,   // v0   v0
		0.5f,   -0.5f,   0.0f,   0.0f,   0.0f,   1.0f,   1.0f,  0.0f,   // v1   v1
		0.5f,   0.5f,    0.0f,   0.0f,   0.0f,   1.0f,   1.0f,  1.0f,   // v2   v2
        // Left Side Triangle 0-2-3 (normals point towards screen)
        -0.5f,  -0.5f,   0.0f,   0.0f,   0.0f,   1.0f,   0.0f,  0.0f,   // v0   v3
        0.5f,   0.5f,    0.0f,   0.0f,   0.0f,   1.0f,   1.0f,  1.0f,   // v2   v4
        -0.5f,  0.5f,    0.0f,   0.0f,   0.0f,   1.0f,   0.0f,  1.0f,   // v3   v5
	};

    mesh.indices = {
		// 2 triangles
		0, 1, 2,    // right
		3, 4, 5,    // left
	};

    createVertexArray(mesh);
}
//---------------------------------------------------------------------
// Hill
//---------------------------------------------------------------------
void createHill(Mesh& mesh)
{
    // local/model two-way offsets
    x = 0.65f;   // 2-way horiz offset
    y = 0.5f;  // 1-way vert offset
    z = 0.5f;   // 1-way depth offset

    // Hill: irregular pyramid with 2 congruent front sides and 1 orthogonal back side and a triangular base (normals should point away each front face)
    // 2-3-0 triangle is vertical against the wall
    //               0
    //              /|\
    //             / | \
	//            /  |  \
    //          3/___|___\2
    //           \   |   /
    //            \  |  /
    //             \ | /
    //              \|/
    //               1
    // 1-2-3 triangle is horizontal on the ground

    mesh.verts = {
        //x	    y       z       nx      ny      nz      u       v       // relV absV
        // Right Face Triangle 1-2-0 (normals point towards right screen)
        0.0f,   0.0f,   z,      0.0f,   1.0f,   1.0f,   0.0f,   0.0f,   // v1   v0
        x,      0.0f,   0.0f,   1.0f,   1.0f,   1.0f,   0.5f,   0.0f,   // v2   v1
        0.0f,   y,      0.0f,   1.0f,   1.0f,   1.0f,   0.5f,   1.0f,   // v0   v2
        // Left Face Triangle 3-1-0 (normals point towards left screen)
        -x,     0.0f,   0.0f,   -1.0f,  1.0f,   1.0f,   0.5f,   0.0f,   // v3   v3
        0.0f,   0.0f,   z,      0.0f,   1.0f,   1.0f,   1.0f,   0.0f,   // v1   v4
        0.0f,   y,      0.0f,   1.0f,   1.0f,   1.0f,   0.5f,   1.0f,   // v0   v5
        // Back Face Triangle 2-3-0 (normals point towards back screen)
        x,      0.0f,   0.0f,   1.0f,   1.0f,   1.0f,   0.0f,   0.0f,   // v2   v6
        -x,     0.0f,   0.0f,   -1.0f,  1.0f,   1.0f,   1.0f,   0.0f,   // v3   v7
        0.0f,   y,      0.0f,   0.0f,   1.0f,   1.0f,   0.5f,   1.0f,   // v0   v8
        // Bottom Face Triangle 2-3-1 (normals point towards bottom and no texture on base)
        x,      0.0f,   0.0f,   0.0f,   -1.0f,  0.0f,   0.0f,   0.0f,   // v2   v9
        -x,     0.0f,   0.0f,   0.0f,   -1.0f,  1.0f,   0.0f,   0.0f,   // v3   v10
        0.0f,   0.0f,   z,      0.0f,   -1.0f,  1.0f,   0.0f,   0.0f,   // v1   v11
    };

    mesh.indices = {  // indices for EBO with glDrawElements()
        // 3 side triangles + 1 base triangle
        0, 1, 2,    // right
        3, 4, 5,    // left
        6, 7, 8,    // back
        9, 10, 11,  // base
    };

    /*
    mesh.verts = {
        // 4-Sided Regular (Right) Pyramid
        //        v3------v4
        //        | \    / |
        //        |  \  /  |
        //        |   v0   |
        //        |  /  \  |
        //        | /    \ |
        //        v2------v1

        // Hill: 5 verts (normals should point away from faces)
        //x     y       z       nx      ny      nz      u       v       // no rgba
        // Front Face Triangle (normals point towards screen)
        0.0f,   y,      0.0f,   0.0f,   1.0f,   0.0f,   0.5f,   1.0f,   // v0   // top point shines up
        x,      -y,     z,      0.0f,   0.0f,   1.0f,   1.0f,   0.0f,   // v1
        -x,     -y,     z,      0.0f,   0.0f,   1.0f,   0.0f,   0.0f,   // v2
        // Right Face Triangle (normals point towards right)
        0.0f,   y,      0.0f,   0.0f,   1.0f,   0.0f,   0.5f,   1.0f,   // v0   // top point shines up
        x,      -y,     z,      1.0f,   0.0f,   0.0f,   1.0f,   0.0f,   // v1
        x,      -y,     -z,     1.0f,   0.0f,   0.0f,   0.0f,   0.0f,   // v4
        // Back Face Triangle (normals point towards back)`
        0.0f,   y,      0.0f,   0.0f,   1.0f,   0.0f,   0.5f,   1.0f,   // v0   // top point shines up
        -x,     -y,     -z,     0.0f,   0.0f,   -1.0f,  1.0f,   0.0f,   // v3
        x,      -y,     -z,     0.0f,   0.0f,   -1.0f,  0.0f,   0.0f,   // v4
        // Left Face Triangle (normals point towards left)
        0.0f,   y,      0.0f,   0.0f,   1.0f,   0.0f,   0.5f,   1.0f,   // v0   // top point shines up
        -x,     -y,     -z,     -1.0f,  0.0f,   0.0f,   1.0f,   0.0f,   // v3
        -x,     -y,     z,      -1.0f,  0.0f,   0.0f,   0.0f,   0.0f,   // v2
        // Bottom Face Triangles (normals point towards bottom)
        // right back base triangle
        x,      -y,     z,      0.0f,   -1.0f,   0.0f,  1.0f,   0.0f,   // v1
        -x,     -y,     -z,     0.0f,   -1.0f,   0.0f,  0.0f,   1.0f,   // v3
        x,      -y,     -z,     0.0f,   -1.0f,   0.0f,  1.0f,   1.0f,   // v4
        // left front base triangle
        x,      -y,     z,      0.0f,   -1.0f,   0.0f,  1.0f,   0.0f,   // v1
        -x,     -y,     -z,     0.0f,   -1.0f,   0.0f,  0.0f,   1.0f,   // v3
        -x,     -y,     z,      0.0f,   -1.0f,   0.0f,  0.0f,   0.0f    // v2
    };
    mesh.indices = {
        // hill triangles: 4 sides
        0, 1, 2,    // right side
        0, 2, 3,    // back side
        0, 3, 4,    // left side
        0, 4, 1,    // front side
        // hill base: 2 triangles
        5, 6, 7,    // right base
        7, 8, 5     // left base
    };
    */

    createVertexArray(mesh);
}
//---------------------------------------------------------------------
// Background
//---------------------------------------------------------------------
void createBackground(Mesh& mesh)
{
    float bottom = yGround; // -0.75f
    float top = yGround + 2.0f;
    float right = 2.0f;
    float left = -2.0f;  // width = 4.0f
    float zPos = -1.0f;  // background depth

    // Background: blue X-Y plane with cloud and possible hill (normals point in z-direction)
    // v2-------------v1
    // |               |
    // |               |
    // |               |
    // v3-------------v0

    mesh.verts = {
        //x         y           z       nx      ny      nz      u	   v    
        // bottom-right
        right,      bottom,     zPos,   0.0f,   0.0f,   1.0f,   1.0f,   0.0f,   // v0
        // top-right
        right,      top,        zPos,   0.0f,   0.0f,   1.0f,   1.0f,   1.0f,   // v1
        // top-left
        left,       top,        zPos,   0.0f,   0.0f,   1.0f,   0.0f,   1.0f,   // v2
        // bottom-left
        left,       bottom,     zPos,   0.0f,   0.0f,   1.0f,   0.0f,   0.0f    // v3

        ////x             y         z           r       g       b       a       u       v
        //// bottom-right
        //right,        bottom,     zPindexos,       bu[0],  bu[1],  bu[2],  bu[3],  1.0f,   0.0f,   // vertex 0: cyan
        //// top-right
        //right,        top,        zPos,       1.0f,   1.0f,   1.0f,   1.0f,   1.0f,   1.0f,   // vertex 1: white
        //// top-left
        //left,         top,        zPos,       1.0f,   1.0f,   1.0f,   1.0f,   0.0f,   1.0f,   // vertex 2: white
        //// bottom-left
        //left,         bottom,     zPos,       bu[0],  bu[1],  bu[2],  bu[3],  0.0f,   0.0f    // vertex 3: cyan
    };

    mesh.indices = {
        // rectangle: 2 triangles
        0, 1, 2,
        0, 2, 3
    };

    createVertexArray(mesh);
}
//---------------------------------------------------------------------
// Ground
// ---------------------------------------------------------------------
void createGround(Mesh& mesh)
{
    float length = 4.0f;    // length of plane
    float halfLength = length / 2.0f;
    float depth = 2.0f;     // width of plane
    float halfDepth = depth / 2.0f;

    // Ground: tiled X-Z plane (normals point up)
    // v2-------------v1
    // |               |
    // |               |
    // |               |
    // v3-------------v0

    groundMesh.verts = {
        //x             y           z           nx      ny      nz      u       v
        // front-right
        halfLength,     yGround,    halfDepth,  0.0f,   1.0f,   0.0f,   20.0f,  0.0f,    // vertex 0: light gray
        // back-right
        halfLength,     yGround,    -halfDepth, 0.0f,   1.0f,   0.0f,   20.0f,  10.0f,   // vertex 1: white
        // back-left
        -halfLength,    yGround,    -halfDepth, 0.0f,   1.0f,   0.0f,   0.0f,   10.0f,   // vertex 2: white
        // front-left
        -halfLength,    yGround,    halfDepth,  0.0f,   1.0f,   0.0f,   0.0f,   0.0f     // vertex 3: light gray
    };

    groundMesh.indices = {
        // rectangle: 2 triangles
        0, 1, 2,
        0, 2, 3
    };

    createVertexArray(mesh);
}
//---------------------------------------------------------------------
// Flag
// ---------------------------------------------------------------------
void createFlag(Mesh& mesh)
{
    float s = 0.08f;   // equal length of triangle sides

    // Flag: white 2D triangle (actually an isosceles triangle)
    // v2-------v1
    //    \      |
    //     \     |
    //      \    |
    //	     \   |
    //        \  |
    //         \ |
    //          \|
    //          v0

    mesh.verts = {
        //x     y       z       nx      ny      nz      u       v    
        // bottom-right
        s,      -s,     0.0f,   1.0f,   -1.0f,  1.0f,   1.0f,   0.0f,   // v0
        // top-right
        s,      s,      0.0f,   1.0f,   1.0f,   1.0f,   1.0f,   1.0f,   // v1
        // top-left
        -s,     s,      0.0f,   -1.0f,  0.0f,   1.0f,   0.0f,   1.0f,   // v2
    };

    mesh.indices = {
        // flag: 1 triangle
        0, 1, 2
    };

    createVertexArray(mesh);
}
//---------------------------------------------------------------------
// Text
// ---------------------------------------------------------------------
void createText(Mesh& mesh)
{
    float height = 1.0f;
    float bottom = yGround - height;
    float top = yGround;
    float width = 2.0f;
    float right = width / 2.0f;
    float left = width / -2.0f;
    float zPos1 = 1.0f;
    float zPos2;

    if (!isOrtho)   // 3D perspective projection
        zPos2 = 2.0f; // angle bottom text toward screen
    else            // 2D orthographic projection
        zPos2 = zPos1; // don't angle text for 2D projection

    repositionText = false;

    // Commands : X-Y plane with transparent background (normals toward screen)
    // v2----------v1
    // |            |
    // |		    |
    // |		    |
    // |		    |
    // |		    |
    // v3----------v0  (toward screen)

    mesh.verts = {
        //x     y       z       nx      ny      nz      u	   v    
        // bottom-right
        right,  bottom, zPos2,  0.0f,   0.0f,   1.0f,   1.0f,   0.0f,   // v0
        // top-right
        right,  top,    zPos1,  0.0f,   0.0f,   1.0f,   1.0f,   1.0f,   // v1
        // top-left
        left,   top,    zPos1,  0.0f,   0.0f,   1.0f,   0.0f,   1.0f,   // v2
        // bottom-left
        left,   bottom, zPos2,  0.0f,   0.0f,   1.0f,   0.0f,   0.0f    // v3
    };

    mesh.indices = {
        // rectangle: 2 triangles
        0, 1, 2,
        0, 2, 3
    };

    createVertexArray(mesh);
}
//---------------------------------------------------------------------
// Blocks
// ---------------------------------------------------------------------
void createBlock(Mesh& mesh)
{
    float size = 0.105f; // size x size x size
    float half = size / 2.0f;

    // Blocks: flag base block and steps
    //    v6----- v5
    //   /|      /|
    //  v2------v1|
    //  | |     | |
    //  | |v7---|-|v4
    //  |/      |/
    //  v3------v0

    mesh.verts = {
        //x     y       z       nx      ny      nz      u       v
        // Front face (v0, v1, v2, v3)
        half,   -half,  half,   0.0f,   0.0f,   1.0f,   1.0f,   0.0f,   // v0  v0
        half,   half,   half,   0.0f,   0.0f,   1.0f,   1.0f,   1.0f,   // v1  v1
        -half,  half,   half,   0.0f,   0.0f,   1.0f,   0.0f,   1.0f,   // v2  v2
        -half,  -half,  half,   0.0f,   0.0f,   1.0f,   0.0f,   0.0f,   // v3  v3
        // Back face (v4, v5, v6, v7)
        half,   -half,  -half,  0.0f,   0.0f,   -1.0f,  0.0f,   0.0f,   // v4  v4
        half,   half,   -half,  0.0f,   0.0f,   -1.0f,  0.0f,   1.0f,   // v5  v5
        -half,  half,   -half,  0.0f,   0.0f,   -1.0f,  1.0f,   1.0f,   // v6  v6
        -half,  -half,  -half,  0.0f,   0.0f,   -1.0f,  1.0f,   0.0f,   // v7  v7
        // Top Face (v2, v6, v5, v1)
        -half,  half,   half,   0.0f,   1.0f,   0.0f,   0.0f,   0.0f,   // v2  v8
        -half,  half,   -half,  0.0f,   1.0f,   0.0f,   0.0f,   1.0f,   // v6  v9
         half,  half,   -half,  0.0f,   1.0f,   0.0f,   1.0f,   1.0f,   // v5  v10
         half,  half,   half,   0.0f,   1.0f,   0.0f,   1.0f,   0.0f,   // v1  v11
         // Bottom face (v7, v4, v0, v3)
         -half, -half,  -half,  0.0f,   -1.0f,  0.0f,   0.0f,   1.0f,   // v7 v12
         half,  -half,  -half,  0.0f,   -1.0f,  0.0f,   1.0f,   1.0f,   // v4 v13
         half,  -half,  half,   0.0f,   -1.0f,  0.0f,   1.0f,   0.0f,   // v0 v14
         -half, -half,  half,   0.0f,   -1.0f,  0.0f,   0.0f,   0.0f,   // v3 v15
         // Left face (v7, v3, v2, v6)
        -half,  -half,  -half,  -1.0f,  0.0f,   0.0f,   0.0f,   0.0f,   // v7  v16
        -half,  -half,  half,   -1.0f,  0.0f,   0.0f,   1.0f,   0.0f,   // v3  v17
        -half,  half,   half,   -1.0f,  0.0f,   0.0f,   1.0f,   1.0f,   // v2  v18
        -half,  half,   -half,  -1.0f,  0.0f,   0.0f,   0.0f,   1.0f,   // v6  v19
        // Right face (v0, v4, v5, v1)
        half,   -half,  half,   1.0f,   0.0f,   0.0f,   0.0f,   0.0f,   // v0  v20
        half,   -half,  -half,  1.0f,   0.0f,   0.0f,   1.0f,   0.0f,   // v4  v21
        half,   half,   -half,  1.0f,   0.0f,   0.0f,   1.0f,   1.0f,   // v5  v22
        half,   half,   half,   1.0f,   0.0f,   0.0f,   0.0f,   1.0f,   // v1  v23
    };

    mesh.indices = {
        // 6 sides * 2 triangles per side = 12 triangles * 3 vertices = 36 vertices
        // Front face
        0, 1, 2,    
        0, 2, 3,    
        // Back face
        5, 4, 7,    
        5, 7, 6,    
        // Top face
        8, 9 ,10,   
        8, 10, 11,  
        // Bottom side
        12, 13, 15, 
        13, 14, 15, 
        // Left side
        16, 18, 19, 
        16, 17, 18, 
        // Right side
        23, 21, 22, 
        23, 21, 20, 
    };

    createVertexArray(mesh);
}
//---------------------------------------------------------------------
// Pole
// ---------------------------------------------------------------------
void createPole(Mesh& mesh)
{
    // *** CUSTOMIZE *** (higher numSides = smoother prism/cylinder)
    const int numSides = 36;  // numSides excludes top and bottom face
    float radius = 0.01f;     // thin pole
    float length = 0.9f;      // (height) tall pole

    // calculations
    float halfLen = length / 2.0f;
    const int numVertices = floatsPerVertex * (2 + (2 * numSides));
    const int numIndices = 12 * numSides;
    //GLfloat verts[numVertices];     // (x,y,z,nx,ny,nz,u,v)
    //GLushort indices[numIndices];   // index used to share vertex position data
    mesh.verts.resize(numVertices);
    mesh.indices.resize(numIndices);

    // creates verts and indices for prism (cylinder)
    //createPrism(verts, indices, numSides, radius, halfLen);
    createPrism(mesh, numSides, radius, halfLen);

    createVertexArray(mesh);
}
//---------------------------------------------------------------------
// Bottom Pipe
// ---------------------------------------------------------------------
void createBottomPipe(Mesh& mesh)
{
    // *** CUSTOMIZE *** (higher numSides = smoother prism/cylinder)
    const int numSides = 36;    // numSides excludes top and bottom face
    float radius = 0.15f;       // thick pipe (little thinner than top pipe)
    float length = 0.12f;       // (height) short pipe

    // calculations
    float halfLen = length / 2.0f;
    const int numVertices = floatsPerVertex * (2 + (2 * numSides));
    const int numIndices = 12 * numSides;
    //GLfloat verts[numVertices];     // (x,y,z,nx,ny,nz,u,v)
    //GLushort indices[numIndices];   // index used to share vertex position data
    mesh.verts.resize(numVertices);
    mesh.indices.resize(numIndices);

    // creates verts and indices for prism (cylinder)
    //createPrism(verts, indices, numSides, radius, halfLen);
    createPrism(mesh, numSides, radius, halfLen);

    createVertexArray(mesh);
}
//---------------------------------------------------------------------
// Top Pipe
// ---------------------------------------------------------------------
void createTopPipe(Mesh& mesh)
{
    // *** CUSTOMIZE *** (higher numSides = smoother prism/cylinder)
    const int numSides = 36;    // numSides excludes top and bottom face
    float radius = 0.18f;       // thick pipe (little thicker than bottom pipe)
    float length = 0.12f;       // (height) short pipe

    // calculations
    float halfLen = length / 2.0f;
    const int numVertices = floatsPerVertex * (2 + (2 * numSides));
    const int numIndices = 12 * numSides;
    //GLfloat verts[numVertices];     // (x,y,z,nx,ny,nz,u,v)
    //GLushort indices[numIndices];   // index used to share vertex position data
    mesh.verts.resize(numVertices);
    mesh.indices.resize(numIndices);

    // creates verts and indices for prism (cylinder)
    //createPrism(verts, indices, numSides, radius, halfLen);
    createPrism(mesh, numSides, radius, halfLen);

    createVertexArray(mesh);
}
//---------------------------------------------------------------------
// Prism/Cylinder
// ---------------------------------------------------------------------
void createPrism(Mesh& mesh, int numSides, float radius, float halfLen)
{
    // constants
    const float TWO_PI = 2.0f * 3.1415926f;
    const float radiansPerSide = TWO_PI / numSides;
    int currentVertex = 0;
    int currentTriangle = 0;

    // create vertex 0 (top center) and vertex 1 (bottom center) with each offset by step size
                        // vertex 0
    mesh.verts[0] = 0.0f;    // 0 x
    mesh.verts[1] = halfLen; // 0 y
    mesh.verts[2] = 0.0f;    // 0 z
    mesh.verts[3] = 1.0f;    // 0 nx
    mesh.verts[4] = 1.0f;    // 0 ny
    mesh.verts[5] = 1.0f;    // 0 nz
    mesh.verts[6] = 1.0f;    // 0 u
    mesh.verts[7] = 1.0f;    // 0 v

    currentVertex++;    // vertex 1
    mesh.verts[8] = 0.0f;     // 1 x
    mesh.verts[9] = -halfLen; // 1 y
    mesh.verts[10] = 0.0f;    // 1 z
    mesh.verts[11] = -1.0f;   // 1 nx
    mesh.verts[12] = -1.0f;   // 1 ny
    mesh.verts[13] = -1.0f;   // 1 nz
    mesh.verts[14] = 0.0f;    // 1 u
    mesh.verts[15] = 0.0f;    // 1 v

    currentVertex++;    // vertex 2
    // note: number of flat sides is equal to the number of edge on the sides
    for (int edge = 0; edge < numSides; edge++)
    {
        // calculate theta, which is the angle from the center point to the next vertex
        float theta = ((float)edge) * radiansPerSide;

        // top triangle first perimeter vertex
        // complete vertex 2 * totalFloatsPer 8 + offset 0.. = mesh.verts[16] x -> mesh.verts[17] y -> mesh.verts[18] z ...
        mesh.verts[currentVertex * floatsPerVertex + 0] = radius * cos(theta);    // x
        mesh.verts[currentVertex * floatsPerVertex + 1] = halfLen;                // y
        mesh.verts[currentVertex * floatsPerVertex + 2] = radius * sin(theta);    // z
        mesh.verts[currentVertex * floatsPerVertex + 3] = 1.0f;                   // nx = right
        mesh.verts[currentVertex * floatsPerVertex + 4] = 1.0f;				      // ny = up
        mesh.verts[currentVertex * floatsPerVertex + 5] = 1.0f;                   // nz = forward (normals = average of 3 normals)
        mesh.verts[currentVertex * floatsPerVertex + 6] = 0.5f;                   // u = halway across
        mesh.verts[currentVertex * floatsPerVertex + 7] = 1.0f;                   // v = top

        currentVertex++;  // vertex 3
        // bottom triangle first perimeter vertex
        mesh.verts[currentVertex * floatsPerVertex + 0] = radius * cos(theta);    // x
        mesh.verts[currentVertex * floatsPerVertex + 1] = -halfLen;               // y
        mesh.verts[currentVertex * floatsPerVertex + 2] = radius * sin(theta);    // z
        mesh.verts[currentVertex * floatsPerVertex + 3] = 1.0f;				      // nx (normals same as top half to avoid tone mismatch)
        mesh.verts[currentVertex * floatsPerVertex + 4] = 1.0f;				      // ny
        mesh.verts[currentVertex * floatsPerVertex + 5] = 1.0f;                   // nz
        mesh.verts[currentVertex * floatsPerVertex + 6] = 0.5f;                   // u = halway across
        mesh.verts[currentVertex * floatsPerVertex + 7] = 0.0f;                   // v = bottom

        currentVertex++;  // vertex 4
        if (edge > 0)
        {
            // create mesh.indices for the triangles
            // top triangle (triangle 0)
            // verticesPerTriangle 3 * currentTriangle 0 + offset 0.. = mesh.indices[0] 0 -> mesh.indices[1] -> mesh.indices[3]
            mesh.indices[(3 * currentTriangle) + 0] = 0;                 // center top vertex  // currentTriangle = 0 (1st pass)  // 3 vertices per triangle
            mesh.indices[(3 * currentTriangle) + 1] = currentVertex - 4; // upper left vertex of side
            mesh.indices[(3 * currentTriangle) + 2] = currentVertex - 2; // upper right vertex of side

            currentTriangle++; // triangle 1
            // bottom triangle
            mesh.indices[(3 * currentTriangle) + 0] = 1;                 // center bottom
            mesh.indices[(3 * currentTriangle) + 1] = currentVertex - 3; // 1; // bottom left vertex of side
            mesh.indices[(3 * currentTriangle) + 2] = currentVertex - 1; // +1; // bottom right vertex of side

            currentTriangle++;  // triangle 2
            // triangle for first 1/2 rectangular side
            mesh.indices[(3 * currentTriangle) + 0] = currentVertex - 4; // upper left vertex of side
            mesh.indices[(3 * currentTriangle) + 1] = currentVertex - 3; // bottom left vertex of side
            mesh.indices[(3 * currentTriangle) + 2] = currentVertex - 1; //; // bottom right vertex of side

            currentTriangle++;  // triangle 3
            // triangle for second 1/2 rectangular side
            mesh.indices[(3 * currentTriangle) + 0] = currentVertex - 1; //; // bottom right vertex of side
            mesh.indices[(3 * currentTriangle) + 1] = currentVertex - 2; // 3; // upper right vertex of side
            mesh.indices[(3 * currentTriangle) + 2] = currentVertex - 4; // +1; // upper left vertex of side

            currentTriangle++;  // triangle 4
        }   // now 1 top and bottom slice, as well as the 1 corresponding rectangular side, have been created (4 triangles total)
    }

    // create more mesh.indices for the final triangles
    // top triangle
    mesh.indices[(3 * currentTriangle) + 0] = 0;                 // center of top of prism
    mesh.indices[(3 * currentTriangle) + 1] = currentVertex - 2; // upper left vertex of side
    mesh.indices[(3 * currentTriangle) + 2] = 2;                 // first upper left vertex created, now right
    currentTriangle++;

    // bottom triangle
    mesh.indices[(3 * currentTriangle) + 0] = 1;                 // center of bottom of prism
    mesh.indices[(3 * currentTriangle) + 1] = currentVertex - 1; // bottom left vertex of side
    mesh.indices[(3 * currentTriangle) + 2] = 3;                 // first bottom left vertex created, now right
    currentTriangle++;

    // triangle for 1/2 retangular side
    mesh.indices[(3 * currentTriangle) + 0] = currentVertex - 2; // upper left vertex of side
    mesh.indices[(3 * currentTriangle) + 1] = currentVertex - 1; // bottom left vertex of side
    mesh.indices[(3 * currentTriangle) + 2] = 3;                 // bottom right vertex of side
    currentTriangle++;

    // triangle for second 1/2 retangular side
    mesh.indices[(3 * currentTriangle) + 0] = 3;                 // bottom right vertex of side
    mesh.indices[(3 * currentTriangle) + 1] = 2;                 // upper right vertex of side
    mesh.indices[(3 * currentTriangle) + 2] = currentVertex - 2; // upper left vertex of side
    currentTriangle++;
}
//---------------------------------------------------------------------
// Array/Buffers
//---------------------------------------------------------------------
void createVertexArray(Mesh& mesh)
{
    if (mesh.vao != 0)
        glDeleteVertexArrays(1, &mesh.vao); // delete previous VAO
    if (mesh.vbo != 0)
        glDeleteBuffers(1, &mesh.vbo);      // delete previous VBO
    if (mesh.ebo != 0)
        glDeleteBuffers(1, &mesh.ebo);      // delete previous EBO

    mesh.vertexBytes = mesh.verts.size() * sizeof(GLfloat);
    mesh.indexBytes = mesh.indices.size() * sizeof(GLushort);

    glGenVertexArrays(1, &mesh.vao); // generate 1 vao
    glBindVertexArray(mesh.vao);  // bind vao

    glGenBuffers(1, &mesh.vbo); // generate 1 vbo
    glBindBuffer(GL_ARRAY_BUFFER, mesh.vbo); // bind vbo
    glBufferData(GL_ARRAY_BUFFER, mesh.verts.size() * sizeof(GLfloat), mesh.verts.data(), GL_STATIC_DRAW);  // .data() provides a pointer to the interal array

    glGenBuffers(1, &mesh.ebo); // generate 1 ebo
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, mesh.ebo);  // bind ebo
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, mesh.indices.size() * sizeof(GLushort), mesh.indices.data(), GL_STATIC_DRAW); // sends index data to GPU

    // position
    glVertexAttribPointer(0, floatsPerPosition, GL_FLOAT, GL_FALSE, STRIDE, 0);
    glEnableVertexAttribArray(0);

    // normals
    glVertexAttribPointer(1, floatsPerNormal, GL_FLOAT, GL_FALSE, STRIDE, (void*)(sizeof(float) * floatsPerPosition));
    glEnableVertexAttribArray(1);

    // color
    //glVertexAttribPointer(2, floatsPerColor, GL_FLOAT, GL_FALSE, STRIDE, (void*)(sizeof(float) * (floatsPerPosition + floatsPerNormal)));
    //glEnableVertexAttribArray(2);

    // texture
    glVertexAttribPointer(2, floatsPerTexture, GL_FLOAT, GL_FALSE, STRIDE, (void*)(sizeof(float) * (floatsPerPosition + floatsPerNormal)));
    glEnableVertexAttribArray(2);

    glBindVertexArray(0);   // unbind vao
}
//---------------------------------------------------------------------
// process keyboard input
//---------------------------------------------------------------------
void processInput(GLFWwindow* window)
{
    const float cameraSpeed = 2.5f * deltaTime;

    // esc
    if (glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS)
        glfwSetWindowShouldClose(window, true);
    // movement speed  (DISABLES scroll wheel speed control)
    //if (glfwGetKey(window, GLFW_KEY_LEFT_SHIFT) == GLFW_PRESS)
    //    camera.MovementSpeed = 2.5f;    // faster movement
    //else
    //	camera.MovementSpeed = 1.5f;    // normal movement
    // show commands switch
    //if (glfwGetKey(window, GLFW_KEY_C) == GLFW_PRESS)
    //	showCommands = true;
    //else if (glfwGetKey(window, GLFW_KEY_C) == GLFW_RELEASE)
    //	showCommands = false;
    // perspective/ortho switch
    if (glfwGetKey(window, GLFW_KEY_P) == GLFW_PRESS)
    {
        isOrtho = false; // toggle switches on and off
        repositionText = true;
    }
    else if (glfwGetKey(window, GLFW_KEY_O) == GLFW_PRESS)
    {
        isOrtho = true;
        repositionText = true;
    }
    // w s a d
    if (glfwGetKey(window, GLFW_KEY_W) == GLFW_PRESS)
        camera.ProcessKeyboard(FORWARD, deltaTime);
    //cout << "W" << endl;
    else if (glfwGetKey(window, GLFW_KEY_S) == GLFW_PRESS)
        camera.ProcessKeyboard(BACKWARD, deltaTime);
    else if (glfwGetKey(window, GLFW_KEY_A) == GLFW_PRESS)
        camera.ProcessKeyboard(LEFT, deltaTime);
    else if (glfwGetKey(window, GLFW_KEY_D) == GLFW_PRESS)
        camera.ProcessKeyboard(RIGHT, deltaTime);
    // q e
    else if (glfwGetKey(window, GLFW_KEY_Q) == GLFW_PRESS)
        camera.ProcessKeyboard(UP, deltaTime);
    else if (glfwGetKey(window, GLFW_KEY_E) == GLFW_PRESS)
        camera.ProcessKeyboard(DOWN, deltaTime);
    // arrow keys (turn/pivot)
    else if (glfwGetKey(window, GLFW_KEY_UP) == GLFW_PRESS)
        camera.ProcessMouseMovement(0, 1);
    else if (glfwGetKey(window, GLFW_KEY_DOWN) == GLFW_PRESS)
        camera.ProcessMouseMovement(0, -1);
    else if (glfwGetKey(window, GLFW_KEY_LEFT) == GLFW_PRESS)
        camera.ProcessMouseMovement(-1, 0);
    else if (glfwGetKey(window, GLFW_KEY_RIGHT) == GLFW_PRESS)
        camera.ProcessMouseMovement(1, 0);
    else if (glfwGetKey(window, GLFW_KEY_G) == GLFW_PRESS)
        yCheck = false;
    else if (glfwGetKey(window, GLFW_KEY_F) == GLFW_PRESS)
        yCheck = true;
    //else keypress = false;

    // does not allow going below ground level
    if (yCheck)
    {
        if (camera.Position.y < yGround + 0.1f)
            camera.Position.y = yGround + 0.1f;  // little Mario eye-level
    }
}
//---------------------------------------------------------------------
// mouse scroll wheel callback
//---------------------------------------------------------------------
void mouseScrollCallback(GLFWwindow* window, double xoffset, double yoffset)
{   // DISABLED when LEFT_SHIFT speed control enabled
    //camera.ProcessMouseScroll(yoffset);
    //cout << "Mouse scrolled: " << yoffset << endl;

    // scroll wheel increases/decreases movement speed
    camera.MovementSpeed += yoffset;
    if (camera.MovementSpeed < 0.1f)
        camera.MovementSpeed = 0.1f;        // lower limit
    else if (camera.MovementSpeed > 100.0f)
        camera.MovementSpeed = 100.0f;      // upper limit

    /*
    // set mouse sensitivity
    float sensitivity = 0.1f;
    xoffset *= sensitivity;
    yoffset *= sensitivity;
    */
}
//---------------------------------------------------------------------
// mouse position callback
//---------------------------------------------------------------------
void mousePositionCallback(GLFWwindow* window, double xpos, double ypos)
{
    if (firstMouse)
    {
        lastX = xpos;
        lastY = ypos;
        firstMouse = false;
    }

    // calculate the mouse's offset since the last frame
    float xoffset = xpos - lastX;
    float yoffset = lastY - ypos;	// reversed since y-coordinates range from bottom to top
    lastX = xpos;
    lastY = ypos;

    // update camera rotation using mouse offset
    camera.ProcessMouseMovement(xoffset, yoffset);
}
//---------------------------------------------------------------------
// mouse button callback
//--------------------------------------------------------------------
void mouseButtonCallback(GLFWwindow* window, int button, int action, int mods)
{
    switch (button)
    {
    case GLFW_MOUSE_BUTTON_LEFT:
        break;
    case GLFW_MOUSE_BUTTON_RIGHT:
        break;
    case GLFW_MOUSE_BUTTON_MIDDLE:
        break;
    default:
        break;
    }
}
//---------------------------------------------------------------------
// create texture
//---------------------------------------------------------------------
bool UCreateTexture(const char* filename, GLuint& textureId)
{
    // load image file
    int width, height, channels;
    if (filename == "../OpenGLSample/images/brick_texture.jpg" || filename == "../OpenGLSample/images/hill_texture.jpg")
        stbi_set_flip_vertically_on_load(false);
    else
        stbi_set_flip_vertically_on_load(true);

    unsigned char* image = stbi_load(filename, &width, &height, &channels, 0);

    if (image)
    {
        glGenTextures(1, &textureId);  // creates 1 texture object and assigns to ID
        glBindTexture(GL_TEXTURE_2D, textureId);  // bind textureId to target GL_TEXTURE_2D

        // set the texture wrapping parameters for target GL_TEXTURE_2D (textureId)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);   // GL_REPEAT repeats texture if outside 0.0f to 1.0f range
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);   // GL_REPEAT, GL_MIRRORED_REPEAT, GL_CLAMP_TO_EDGE, GL_CLAMP_TO_BORDER
        // set texture filtering parameters for target GL_TEXTURE_2D (textureId)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);   // GL_LINEAR interpolates (smoothes) minified textures (displayed smaller than actual size)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);   // linear interpolation for magnified textures (displayed larger than actual size)

        // image information
        cout << "Image loaded: " << filename << endl;
        cout << "Image width: " << width << endl;
        cout << "Image height: " << height << endl;
        cout << "Image channels: " << channels << endl;

        // 3 channels = RGB or sRGB, 4 channels = RGBA or sRGBA
        /*
        GLenum format;
        if (channels == 1)
            format = GL_RED;
        else if (channels == 3) // no alpha channel
            format = GL_RGB;
        else if (channels == 4) // alpha channel
            format = GL_RGBA;
        */
        if (channels == 3) // no alpha channel
        {
            glTexImage2D(GL_TEXTURE_2D, 0, GL_SRGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, image);
            glEnable(GL_FRAMEBUFFER_SRGB); // TODO: SRGB gamma correction
            //glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB8, width, height, 0, GL_RGB8, GL_UNSIGNED_BYTE, image);
        }
        else if (channels == 4) // alpha channel
        {
            //glTexImage2D(GL_TEXTURE_2D, 0, GL_SRGB_ALPHA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image);
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image);
            glDisable(GL_FRAMEBUFFER_SRGB); // SRGB gamma correction off
            //glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA8, width, height, 0, GL_RGBA8, GL_UNSIGNED_BYTE, image);
        }
        else
        {
            cout << "Not implemented to handle image with " << channels << " channels" << endl;
            return false;
        }
        if (firstLoop)
            cout << "Texture bound successfully!\n" << endl;

        glGenerateMipmap(GL_TEXTURE_2D);

        stbi_image_free(image);
        glBindTexture(GL_TEXTURE_2D, 0); // Unbind the texture

        return true;
    }

    // Error loading the image
    return false;
}
//---------------------------------------------------------------------
// GLFW, GLAD, and OpenGL initialization & window creation
//---------------------------------------------------------------------
bool UInitialize(int argc, char* argv[], GLFWwindow** window)
{
    // GLFW: initialize and configure
    // ------------------------------
    glfwInit();
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 4);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 6);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

#ifdef __APPLE__
    glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);
#endif

    // GLFW: window creation
    // ---------------------
    * window = glfwCreateWindow(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, NULL, NULL);
    if (*window == NULL)
    {
        std::cout << "Failed to create GLFW window" << std::endl;
        glfwTerminate();
        return false;
    }
    glfwMakeContextCurrent(*window);
    glfwSetFramebufferSizeCallback(*window, UResizeWindow);
    glfwSetScrollCallback(*window, mouseScrollCallback);
    glfwSetCursorPosCallback(*window, mousePositionCallback);
    glfwSetMouseButtonCallback(*window, mouseButtonCallback);
    glfwSetInputMode(*window, GLFW_CURSOR, GLFW_CURSOR_DISABLED);

    // GLAD: load all OpenGL function pointers
    if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress))
    {
        cerr << "Failed to initialize GLAD" << endl;
        return false;
    }

    // Displays GPU OpenGL version
    cout << "INFO: OpenGL Version: " << glGetString(GL_VERSION) << endl << endl;

    return true;
}
//---------------------------------------------------------------------
// destroy mesh after rendering
//---------------------------------------------------------------------
void cleanUp()
{
    for (Mesh& mesh : meshes) {
        glDeleteVertexArrays(1, &mesh.vao);
        glDeleteBuffers(1, &mesh.vbo);
        glDeleteBuffers(1, &mesh.ebo);
    }

    for (GLuint& textureId : textureIds) {
        glDeleteTextures(1, &textureId);
    }
}
//---------------------------------------------------------------------
// resize window if initiated
//---------------------------------------------------------------------
void UResizeWindow(GLFWwindow* window, int width, int height)
{
    glViewport(0, 0, width, height);
}
