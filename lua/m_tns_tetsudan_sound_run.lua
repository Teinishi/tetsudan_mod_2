RADIUS_INNER = 20
RADIUS_OUTER = 200
SPEED_MAX_VOLUME = 50

local function clamp(x, a, b)
    return math.min(math.max(x, a), b)
end

local sfx_state = {}

local function sfx_start(channel, index, volume, pitch)
    if component.sfxPlayLoop(channel, index, 0, 0, 0, RADIUS_INNER, RADIUS_OUTER, volume, pitch, 1) then
        sfx_state[channel] = index
    end
end

local function sfx_stop(channel)
    if component.sfxStop(channel) then
        sfx_state[channel] = nil
    end
end

local function sfx_update(channel, index, volume, pitch)
    if sfx_state[channel] == index then
        component.sfxUpdate(channel, 0, 0, 0, RADIUS_INNER, RADIUS_OUTER, volume, pitch)
    else
        sfx_stop(channel)
        if sfx_state[channel] == nil then
            sfx_start(channel, index, volume, pitch)
        end
    end
end

function onTick()
    local composite, success = component.getInputLogicSlotComposite(0)
    if success then
        local fv = composite.float_values
        for i = 0, 3 do
            local index = math.floor(fv[2 * i + 1] + 0.5)
            local speed = fv[2 * i + 2] * 3.6
            local base = BASE_SPEED[index]

            if base ~= nil then
                local pitch = speed / base
                local volume = clamp((speed - 0.1 * base) / (0.4 * base), 0, 1)
                if volume > 0 then
                    sfx_update(i, index - 1, volume, pitch)
                else
                    sfx_stop(i)
                end
            else
                sfx_stop(i)
            end
        end
    end
end

function onRemoveFromSimulation()
    for i = 0, 3 do
        component.sfxStop(i)
    end
end

