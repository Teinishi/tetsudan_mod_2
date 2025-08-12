RADIUS_INNER = 10
RADIUS_OUTER = 150

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

        for channel = 0, 3 do
            local index, volume, pitch = nil, 0, 0
            for i = channel, N - 1, 4 do
                local v = clamp(fv[2 * i + 1], 0, 1)
                if v ~= 0 and v >= volume then
                    index = i
                    volume = v
                    pitch = math.max(fv[2 * i + 2], 0)
                end
            end

            if index == nil then
                sfx_stop(channel)
            else
                sfx_update(channel, index, volume, pitch)
            end
        end
    end
end

function onRemoveFromSimulation()
    for i = 0, 3 do
        component.sfxStop(i)
    end
end
